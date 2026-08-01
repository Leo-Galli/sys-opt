# -*- coding: utf-8 -*-
"""
sys-opt benchmark: lightweight CPU / RAM / disk stress tests (psutil-backed).

Every measurement is wrapped in try/except (zero-crash policy) and degrades
to 0.0 / 'N/A' instead of crashing. Results are rendered in a comparative
rich table with a trend bar, or as JSON with ``--json``.
"""

import json
import os
import tempfile
import time

try:
    import psutil
except Exception:  # pragma: no cover - optional dependency
    psutil = None

from rich.panel import Panel
from rich.table import Table

from .utils import config_dir, format_bytes

_BAR_WIDTH = 12

#: Reference thresholds (slow, good, great) per metric — used only for the
#: plain-table verdict, never for the JSON payload. Calibrated against real
#: measurements: the CPU loop is a Python tight loop (a few M ops/s), RAM is
#: memcpy bandwidth, disk is sequential temp-file I/O.
_REFERENCE = {
    "cpu_mops": (2.0, 4.0, 8.0),
    "ram_mbps": (4000.0, 8000.0, 15000.0),
    "disk_write_mbps": (150.0, 400.0, 900.0),
    "disk_read_mbps": (200.0, 500.0, 1200.0),
}

_VERDICT_KEYS = {
    0: "benchmark_verdict_slow",
    1: "benchmark_verdict_ok",
    2: "benchmark_verdict_good",
    3: "benchmark_verdict_great",
}


def _cpu_benchmark(duration=1.0):
    """Light CPU compute stress; returns M ops/s (millions of ops per sec)."""
    start = time.perf_counter()
    ops = 0
    x = 1.0000001
    end = start + duration
    while time.perf_counter() < end:
        x = x * 1.0000001 + 0.0000001
        x = x - 0.00000005
        ops += 1
    elapsed = time.perf_counter() - start
    if elapsed <= 0:
        return 0.0
    return (ops / elapsed) / 1e6


def _ram_benchmark(size_mb=64, copies=8):
    """Copy a buffer repeatedly; returns MB/s of memory bandwidth."""
    try:
        size = int(size_mb) * 1024 * 1024
        src = bytearray(size)
        dst = bytearray(size)
        start = time.perf_counter()
        for _ in range(int(copies)):
            dst[:] = src
        elapsed = time.perf_counter() - start
        if elapsed <= 0:
            return 0.0
        return (size * int(copies)) / elapsed / (1024 * 1024)
    except Exception:
        return 0.0


def _disk_benchmark(size_mb=32, directory=None):
    """Write then read a temp file; returns (write_mbps, read_mbps)."""
    directory = directory or tempfile.gettempdir()
    path = os.path.join(directory, "sys_opt_benchmark.tmp")
    data = os.urandom(int(size_mb) * 1024 * 1024)
    write_mbps = 0.0
    read_mbps = 0.0
    try:
        start = time.perf_counter()
        with open(path, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        elapsed = time.perf_counter() - start
        if elapsed > 0:
            write_mbps = int(size_mb) / elapsed

        start = time.perf_counter()
        total = 0
        with open(path, "rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
        elapsed = time.perf_counter() - start
        if elapsed > 0:
            read_mbps = (total / (1024 * 1024)) / elapsed
    except Exception:
        pass
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
    return write_mbps, read_mbps


def _context():
    """Small machine context for the header; never raises."""
    context = {}
    if psutil is not None:
        try:
            context["cpu_count"] = psutil.cpu_count(logical=True)
        except Exception:
            context["cpu_count"] = None
        try:
            context["ram_total"] = psutil.virtual_memory().total
        except Exception:
            context["ram_total"] = None
        try:
            context["cpu_name"] = psutil.cpu_info()[0].brand  # not portable
        except Exception:
            context["cpu_name"] = None
    return context


def _trend_bar(value, maximum):
    """Relative ██░░ bar compared to the given maximum (a component in the
    compare table, or the run-window maximum in the history charts)."""
    if maximum <= 0 or value <= 0:
        return "[dim]%s[/]" % ("░" * _BAR_WIDTH)
    filled = int(round(value / maximum * _BAR_WIDTH))
    filled = max(1, min(filled, _BAR_WIDTH))
    return "[green]%s[/][dim]%s[/]" % ("█" * filled, "░" * (_BAR_WIDTH - filled))


#: Metrics shown in the comparison table: (i18n key, result key, fmt).
_COMPARE_METRICS = (
    ("benchmark_cpu", "cpu_mops", "%.2f M ops/s"),
    ("benchmark_ram", "ram_mbps", "%.0f MB/s"),
    ("benchmark_disk_write", "disk_write_mbps", "%.0f MB/s"),
    ("benchmark_disk_read", "disk_read_mbps", "%.0f MB/s"),
)


#: Maximum number of runs kept in the persisted history (oldest dropped).
_HISTORY_MAX = 500


def _baseline_path(base=None):
    """Path of the persisted benchmark history (inside ~/.sys-opt)."""
    return config_dir(base) / "benchmark.json"


def load_history(base=None):
    """Load every saved benchmark run, oldest first; [] on any failure.

    Backward compatible: files written before --history stored a single run
    as a dict ``{timestamp, results}``; those are treated as a one-element
    history. A list is the current format (newest last). Corrupt or
    non-dict entries are dropped so the history never crashes a render.
    """
    try:
        data = json.loads(_baseline_path(base).read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return []
    runs = [entry for entry in data if isinstance(entry, dict)]
    return runs[-_HISTORY_MAX:]


def load_baseline(base=None):
    """Load the most recent saved run (for --compare); {} when none."""
    history = load_history(base)
    return history[-1] if history else {}


def save_baseline(results, base=None):
    """Append a benchmark run (timestamped) to the persisted history.

    Never raises (zero-crash policy): a missing/read-only config dir simply
    means the run is not stored. The newest run is always the last element,
    so ``load_baseline`` keeps returning the latest measurement for --compare.
    """
    try:
        directory = config_dir(base)
        directory.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": results,
        }
        history = load_history(base)
        history.append(payload)
        del history[:-_HISTORY_MAX]  # keep only the newest _HISTORY_MAX runs
        _baseline_path(base).write_text(
            json.dumps(history, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return True
    except Exception:
        return False


def _delta_pct(new_value, old_value):
    """Percentage change of new vs old; None when either is unusable."""
    try:
        new_value = float(new_value)
        old_value = float(old_value)
    except (TypeError, ValueError):
        return None
    if new_value <= 0 or old_value <= 0:
        return None
    return (new_value - old_value) / old_value * 100.0


def _delta_cell(delta):
    """Color-coded Δ cell: green for improvement, red for regression, — when N/A."""
    if delta is None:
        return "[dim]—[/]"
    sign = "+" if delta >= 0 else ""
    color = "green" if delta >= 0 else "red"
    return "[%s]%s%.1f%%[/]" % (color, sign, delta)


def _short_ts(timestamp):
    """'2026-08-01 14:03:22' -> '08-01 14:03'; the raw value on any oddity."""
    try:
        date_part, time_part = str(timestamp).split(" ")[:2]
        return "%s %s" % (date_part[5:], time_part[:5])
    except Exception:
        return str(timestamp)


def _history_trend(current, previous):
    """Trend marker for a run vs the previous one: ▲ green, ▼ red, · flat."""
    if previous is None or current <= 0 or previous <= 0:
        return ""
    if current > previous * 1.01:
        return " [green]▲[/]"
    if current < previous * 0.99:
        return " [red]▼[/]"
    return " [dim]·[/]"


def history(console, t, limit=None, as_json=False, base=None):
    """Render saved benchmark runs as per-metric ASCII trend charts.

    Reads only ``~/.sys-opt/benchmark.json`` (never runs the stress test and
    never writes). With ``as_json`` the raw run list is emitted as pure JSON
    for scripting; otherwise each metric (CPU / RAM / disk write / disk read)
    is drawn as a bar chart, oldest at the top, with ▲/▼/· showing the trend
    from one run to the next.
    """
    runs = load_history(base)
    if limit and limit > 0:
        runs = runs[-limit:]
    if as_json:
        console.file.write(json.dumps(runs, indent=2) + "\n")
        return 0

    console.print()
    console.print(Panel("[bold green]%s[/]" % t("benchmark_history_header"), border_style="green"))
    if not runs:
        console.print()
        console.print("[yellow]%s[/]" % t("benchmark_history_none"))
        return 0
    console.print(
        "[dim]%s[/]" % (t("benchmark_history_runs") % len(runs))
    )

    for label_key, result_key, fmt in _COMPARE_METRICS:
        console.print()
        console.print("[bold]%s[/]" % t(label_key))
        values = []
        for run in runs:
            try:
                raw = run.get("results", {}).get(result_key, 0.0)
                values.append(float(raw) if raw not in (None, "", False) else 0.0)
            except (TypeError, ValueError):
                values.append(0.0)
        maximum = max(values) if values else 0.0
        previous = None
        for run, value in zip(runs, values):
            ts = _short_ts(run.get("timestamp", "?"))
            value_label = fmt % value if value > 0 else t("na")
            line = "  [dim]%s[/]  %10s  %s" % (ts, value_label, _trend_bar(value, maximum))
            line += _history_trend(value, previous)
            console.print(line)
            previous = value
    console.print()
    console.print("[dim]%s[/]" % t("benchmark_history_tip"))
    return 0


def measure():
    """Run the full stress suite once; returns the raw results dict.

    Shared by :func:`run` (table/JSON rendering) and the HTML report flow
    (``report.run_*_report``), so the numbers are identical across modes.
    """
    start = time.perf_counter()
    cpu_mops = _cpu_benchmark()
    ram_mbps = _ram_benchmark()
    write_mbps, read_mbps = _disk_benchmark()
    elapsed = time.perf_counter() - start
    return {
        "cpu_mops": round(cpu_mops, 2),
        "ram_mbps": round(ram_mbps, 1),
        "disk_write_mbps": round(write_mbps, 1),
        "disk_read_mbps": round(read_mbps, 1),
        "elapsed_seconds": round(elapsed, 2),
    }


def _verdict(results):
    """Map results to a verdict i18n key (0=slow .. 3=great).

    The overall score is the *lowest* tier among the measured components:
    a machine is only as fast as its weakest part. Metrics that failed to
    measure (0.0) are skipped.
    """
    scores = []
    for key, thresholds in _REFERENCE.items():
        value = results.get(key, 0.0)
        if value <= 0:
            continue
        slow, good, great = thresholds
        if value >= great:
            score = 3
        elif value >= good:
            score = 2
        elif value >= slow:
            score = 1
        else:
            score = 0
        scores.append(score)
    if not scores:
        return "benchmark_verdict_ok"
    return _VERDICT_KEYS[min(scores)]


def run(console, t, as_json=False, compare=False, base=None, show_history=False, history_limit=None):
    """Run the benchmark suite and print the comparative table.

    With ``compare=True`` (table mode only) the results are appended to the
    persisted history in ``~/.sys-opt/benchmark.json`` and, when a previous
    baseline exists, an extra ``Δ vs baseline`` column shows the percentage
    change per metric — so running it before and after an optimization shows
    the gain at a glance. With ``show_history=True`` the saved runs are
    rendered as per-metric ASCII trend charts (no stress test is run). JSON
    mode stays machine-pure and never writes the history.

    Note: the parameter is ``show_history`` (not ``history``) so it cannot
    shadow the module-level :func:`history` renderer it dispatches to.
    """
    if show_history:
        return history(console, t, limit=history_limit, as_json=as_json, base=base)
    if compare and as_json:
        compare = False  # keep --benchmark --json pure for piping/scripts
    if not as_json:
        context = _context()
        console.print()
        console.print(
            Panel(
                "[bold green]%s[/]" % t("benchmark_header"),
                border_style="green",
            )
        )
        console.print("[dim]%s[/]" % t("benchmark_running"))

    results = measure()
    cpu_mops = results["cpu_mops"]
    ram_mbps = results["ram_mbps"]
    write_mbps = results["disk_write_mbps"]
    read_mbps = results["disk_read_mbps"]
    elapsed = results["elapsed_seconds"]

    if as_json:
        # Raw write (same rationale as inspector): bypass rich's rendering and
        # 80-column wrapping so the JSON stays machine-parseable when piped.
        console.file.write(json.dumps(results, indent=2) + "\n")
        return 0

    baseline = load_baseline(base) if compare else {}
    baseline_results = baseline.get("results") if isinstance(baseline.get("results"), dict) else None
    has_baseline = baseline_results is not None

    header_parts = []
    if context.get("cpu_count"):
        header_parts.append("%d %s" % (context["cpu_count"], t("label_threads")))
    if context.get("ram_total"):
        header_parts.append("%s RAM" % format_bytes(context["ram_total"]))
    if header_parts:
        console.print("[dim]%s[/]" % " · ".join(header_parts))

    maximum = max(cpu_mops, ram_mbps, write_mbps, read_mbps)
    table = Table(
        title="%s · %s: %.1fs" % (t("benchmark_summary"), t("benchmark_elapsed"), elapsed),
        border_style="cyan",
    )
    table.add_column(t("benchmark_col_component"), style="bold")
    table.add_column(t("benchmark_col_result"), justify="right")
    if has_baseline:
        table.add_column(t("benchmark_col_delta"), justify="right")
    table.add_column(t("benchmark_col_trend"), justify="center")
    values = {
        "cpu_mops": cpu_mops,
        "ram_mbps": ram_mbps,
        "disk_write_mbps": write_mbps,
        "disk_read_mbps": read_mbps,
    }
    for label_key, result_key, fmt in _COMPARE_METRICS:
        value = values[result_key]
        cells = [t(label_key), fmt % value if value > 0 else t("na")]
        if has_baseline:
            cells.append(_delta_cell(_delta_pct(value, baseline_results.get(result_key))))
        cells.append(_trend_bar(value, maximum))
        table.add_row(*cells)
    console.print(table)

    if compare:
        console.print()
        console.print("[bold cyan]%s[/]" % t("benchmark_compare_header"))
        if has_baseline:
            console.print(
                "[dim]%s[/]" % (t("benchmark_baseline_from") % baseline.get("timestamp", "?"))
            )
        else:
            console.print("[yellow]%s[/]" % t("benchmark_no_baseline"))
        if save_baseline(results, base=base):
            console.print("[dim]%s[/]" % t("benchmark_baseline_saved"))

    # Explanation + verdict (plain table mode only; --json stays untouched).
    console.print()
    console.print("[bold cyan]%s[/]" % t("benchmark_what"))
    for key in ("benchmark_explain_cpu", "benchmark_explain_ram", "benchmark_explain_disk"):
        console.print("  [dim]•[/] %s" % t(key))
    console.print()
    console.print("[bold]%s[/]" % t(_verdict(results)))
    console.print("[dim]%s[/]" % t("benchmark_tip"))
    return 0
