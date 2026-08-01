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

from .utils import format_bytes

_BAR_WIDTH = 12


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
    """Relative ██░░ bar compared to the fastest measured component."""
    if maximum <= 0 or value <= 0:
        return "[dim]%s[/]" % ("░" * _BAR_WIDTH)
    filled = int(round(value / maximum * _BAR_WIDTH))
    filled = max(1, min(filled, _BAR_WIDTH))
    return "[green]%s[/][dim]%s[/]" % ("█" * filled, "░" * (_BAR_WIDTH - filled))


def run(console, t, as_json=False):
    """Run the benchmark suite and print the comparative table."""
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

    start = time.perf_counter()
    cpu_mops = _cpu_benchmark()
    ram_mbps = _ram_benchmark()
    write_mbps, read_mbps = _disk_benchmark()
    elapsed = time.perf_counter() - start

    results = {
        "cpu_mops": round(cpu_mops, 2),
        "ram_mbps": round(ram_mbps, 1),
        "disk_write_mbps": round(write_mbps, 1),
        "disk_read_mbps": round(read_mbps, 1),
        "elapsed_seconds": round(elapsed, 2),
    }

    if as_json:
        # Raw write (same rationale as inspector): bypass rich's rendering and
        # 80-column wrapping so the JSON stays machine-parseable when piped.
        console.file.write(json.dumps(results, indent=2) + "\n")
        return 0

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
    table.add_column(t("benchmark_col_trend"), justify="center")
    table.add_row(
        t("benchmark_cpu"),
        "%.2f M ops/s" % cpu_mops if cpu_mops > 0 else t("na"),
        _trend_bar(cpu_mops, maximum),
    )
    table.add_row(
        t("benchmark_ram"),
        "%.0f MB/s" % ram_mbps if ram_mbps > 0 else t("na"),
        _trend_bar(ram_mbps, maximum),
    )
    table.add_row(
        t("benchmark_disk_write"),
        "%.0f MB/s" % write_mbps if write_mbps > 0 else t("na"),
        _trend_bar(write_mbps, maximum),
    )
    table.add_row(
        t("benchmark_disk_read"),
        "%.0f MB/s" % read_mbps if read_mbps > 0 else t("na"),
        _trend_bar(read_mbps, maximum),
    )
    console.print(table)
    return 0
