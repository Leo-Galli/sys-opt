# -*- coding: utf-8 -*-
"""Tests for the benchmark module: light stress measurements + table output."""

import os
import tempfile
import unittest

from rich.console import Console

from sys_opt.benchmark import _cpu_benchmark, _disk_benchmark, _ram_benchmark, run
from sys_opt.i18n.languages import build_translator


class TestBenchmark(unittest.TestCase):
    def test_cpu_benchmark_returns_positive(self):
        result = _cpu_benchmark(duration=0.05)
        self.assertGreater(result, 0.0)

    def test_ram_benchmark_returns_positive(self):
        result = _ram_benchmark(size_mb=4, copies=2)
        self.assertGreater(result, 0.0)

    def test_disk_benchmark_returns_pair_and_cleans_up(self):
        with tempfile.TemporaryDirectory() as directory:
            write_mbps, read_mbps = _disk_benchmark(size_mb=2, directory=directory)
            self.assertGreaterEqual(write_mbps, 0.0)
            self.assertGreaterEqual(read_mbps, 0.0)
            leftover = os.path.join(directory, "sys_opt_benchmark.tmp")
            self.assertFalse(os.path.exists(leftover))

    def test_disk_benchmark_never_raises(self):
        write_mbps, read_mbps = _disk_benchmark(size_mb=1, directory="/nonexistent/xyz")
        self.assertGreaterEqual(write_mbps, 0.0)
        self.assertGreaterEqual(read_mbps, 0.0)

    def test_run_returns_zero_and_renders_table(self):
        from io import StringIO

        stream = StringIO()
        console = Console(file=stream, force_terminal=True, width=100)
        t = build_translator("en")
        rc = run(console, t)
        output = stream.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("Performance Benchmark", output)
        self.assertIn("CPU", output)
        self.assertIn("MB/s", output)

    def test_run_json_mode(self):
        import json as jsonlib
        from io import StringIO

        stream = StringIO()
        console = Console(file=stream, force_terminal=True, width=100)
        t = build_translator("en")
        rc = run(console, t, as_json=True)
        data = jsonlib.loads(stream.getvalue())
        self.assertEqual(rc, 0)
        for key in ("cpu_mops", "ram_mbps", "disk_write_mbps", "disk_read_mbps", "elapsed_seconds"):
            self.assertIn(key, data)


if __name__ == "__main__":
    unittest.main()
