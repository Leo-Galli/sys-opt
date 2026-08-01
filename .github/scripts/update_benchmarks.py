#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge nightly benchmark artifacts into benchmarks/ and regenerate report.md.

Usage: python .github/scripts/update_benchmarks.py <artifacts-dir>

Each artifact is a file named ``bench-<os>.json`` containing the JSON emitted
by ``sys-opt --benchmark --json`` (cpu_mops, ram_mbps, disk_write_mbps,
disk_read_mbps, elapsed_seconds). Every run is appended to
``benchmarks/<os>.json`` (kept to the latest MAX_RUNS entries) and
``benchmarks/report.md`` is regenerated with a comparative table of the latest
run per OS plus the recent history per OS. Pure standard library, zero deps.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BENCH_DIR = ROOT / "benchmarks"
MAX_RUNS = 365

# (json_key, human label, unit, decimals)
METRICS = (
    ("cpu_mops", "CPU", "M ops/s", 1),
    ("ram_mbps", "RAM", "MB/s", 0),
    ("disk_write_mbps", "Disk write", "MB/s", 0),
    ("disk_read_mbps", "Disk read", "MB/s", 0),
    ("elapsed_seconds", "Elapsed", "s", 1),
)

#: Reference thresholds (slow, good, great) per metric, used only to build
#: the per-OS verdict in the report. Matches sys_opt/benchmark.py heuristics.
_REFERENCE = {
    "cpu_mops": (2.0, 4.0, 8.0),
    "ram_mbps": (4000.0, 8000.0, 15000.0),
    "disk_write_mbps": (150.0, 400.0, 900.0),
    "disk_read_mbps": (200.0, 500.0, 1200.0),
}

_VERDICTS = {
    0: ("🔴 Below average", "consider running the optimizer"),
    1: ("🟡 Average", "an optimization run may help"),
    2: ("🟢 Good", "running well"),
    3: ("🟢 Excellent", "performing very well"),
}


def _verdict(record):
    """Return (label, note) describing the overall machine health.

    The score is the lowest tier among the measured components (a machine is
    only as fast as its weakest part); unmeasured metrics (<= 0) are skipped.
    """
    scores = []
    for key, (slow, good, great) in _REFERENCE.items():
        value = record.get(key, 0.0)
        if not isinstance(value, (int, float)) or value <= 0:
            continue
        if value >= great:
            scores.append(3)
        elif value >= good:
            scores.append(2)
        elif value >= slow:
            scores.append(1)
        else:
            scores.append(0)
    if not scores:
        return _VERDICTS[1]
    return _VERDICTS[min(scores)]


def _utc_now():
    return datetime.now(timezone.utc)


def _fmt(value, unit, digits):
    if isinstance(value, (int, float)) and value > 0:
        return "%s %s" % (format(value, ".%df" % digits), unit)
    return "N/A"


def _read_history(path):
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _write_report(all_runs):
    lines = [
        "# 📊 sys-opt Nightly Benchmark",
        "",
        "Automated **CPU / RAM / disk** benchmarks (light stress via `psutil`) run every night on",
        "**Linux, macOS and Windows** (GitHub-hosted runners). Each run is appended to",
        "`benchmarks/<os>.json`; this report shows the latest run per OS and the recent history.",
        "",
        "_Last update: %s UTC_" % _utc_now().strftime("%Y-%m-%d %H:%M"),
        "",
        "## Latest run per OS",
        "",
    ]
    ordered = sorted(all_runs)
    lines.append("| Metric | " + " | ".join("**%s**" % os_name for os_name in ordered) + " | Unit |")
    lines.append("|" + "---|" * (len(ordered) + 2))
    for key, label, unit, digits in METRICS:
        row = ["| %s" % label]
        for os_name in ordered:
            history = all_runs[os_name]
            latest = history[-1] if history else {}
            row.append(_fmt(latest.get(key), unit, digits))
        # Real markdown cells: join with " | " (a single-space join would
        # render every metric as one big cell, breaking the table layout).
        lines.append(" | ".join(row) + " |")
    verdict_row = ["| **Overall verdict**"]
    for os_name in ordered:
        history = all_runs[os_name]
        latest = history[-1] if history else {}
        label, _note = _verdict(latest)
        verdict_row.append(label)
    lines.append(" | ".join(verdict_row) + " |")
    lines.extend(
        [
            "",
            "## How to read these numbers",
            "",
            "| Metric | Meaning | Higher is |",
            "|---|---|---|",
            "| **CPU** | Floating-point operations per second (light compute loop) | better |",
            "| **RAM** | Memory bandwidth measured with repeated buffer copies | better |",
            "| **Disk write / read** | Sequential temp-file write/read speed (fsync included) | better |",
            "| **Elapsed** | Total time the whole benchmark took | lower is better |",
            "",
            "The **overall verdict** is the *lowest* tier among the measured",
            "components: a machine is only as fast as its weakest part. Expect",
            "realistic numbers on a GitHub-hosted runner to land in the",
            "**Average** band — that is the baseline.",
            "",
            "Run `python -m sys_opt --benchmark` on your own machine **before**",
            "optimizing to get a baseline, then again **after** to measure the",
            "improvement.",
            "",
            "## Recent history",
            "",
        ]
    )
    for os_name in ordered:
        lines.extend(["### %s" % os_name, ""])
        history = all_runs[os_name]
        if not history:
            lines.extend(["_No runs recorded yet._", ""])
            continue
        lines.append("| Date (UTC) | CPU (M ops/s) | RAM (MB/s) | Write (MB/s) | Read (MB/s) | Elapsed (s) |")
        lines.append("|---|---|---|---|---|---|")
        for record in history[-14:]:
            lines.append(
                "| %s | %s | %s | %s | %s | %s |"
                % (
                    record.get("timestamp", "?"),
                    _fmt(record.get("cpu_mops"), "", 2),
                    _fmt(record.get("ram_mbps"), "", 0),
                    _fmt(record.get("disk_write_mbps"), "", 0),
                    _fmt(record.get("disk_read_mbps"), "", 0),
                    _fmt(record.get("elapsed_seconds"), "", 1),
                )
            )
        lines.append("")
    BENCH_DIR.joinpath("report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv):
    artifacts = Path(argv[1]) if len(argv) > 1 else Path("artifacts")
    files = sorted(artifacts.glob("bench-*.json"))
    if not files:
        print("No bench-*.json artifacts found in %s" % artifacts, file=sys.stderr)
        return 1
    BENCH_DIR.mkdir(exist_ok=True)
    all_runs = {}
    for path in files:
        match = re.match(r"^bench-(.+)\.json$", path.name)
        if not match:
            continue
        os_name = match.group(1)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print("Skipping %s: %s" % (path.name, exc), file=sys.stderr)
            continue
        record = {
            "timestamp": _utc_now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
            "os": os_name,
        }
        record.update(payload)
        history_path = BENCH_DIR / (os_name + ".json")
        history = _read_history(history_path)
        history.append(record)
        del history[:-MAX_RUNS]
        history_path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
        all_runs[os_name] = history
        print("Appended %s -> benchmarks/%s.json (now %d runs)" % (path.name, os_name, len(history)))
    _write_report(all_runs)
    print("Regenerated benchmarks/report.md for: %s" % ", ".join(sorted(all_runs)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
