# -*- coding: utf-8 -*-
"""Tests for the benchmark module: light stress measurements + table output."""

import os
import tempfile
import unittest

from rich.console import Console

from sys_opt.benchmark import (
    _cpu_benchmark,
    _delta_pct,
    _disk_benchmark,
    _ram_benchmark,
    _verdict,
    load_baseline,
    run,
    save_baseline,
)
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

    def test_verdict_maps_to_expected_key(self):
        """The verdict follows the *weakest* measured component."""
        great = {"cpu_mops": 10.0, "ram_mbps": 20000.0, "disk_write_mbps": 1500.0, "disk_read_mbps": 3000.0}
        good = {"cpu_mops": 6.0, "ram_mbps": 12000.0, "disk_write_mbps": 1000.0, "disk_read_mbps": 3000.0}
        ok = {"cpu_mops": 3.0, "ram_mbps": 6000.0, "disk_write_mbps": 600.0, "disk_read_mbps": 800.0}
        slow = {"cpu_mops": 1.0, "ram_mbps": 3000.0, "disk_write_mbps": 100.0, "disk_read_mbps": 150.0}
        self.assertEqual(_verdict(great), "benchmark_verdict_great")
        self.assertEqual(_verdict(good), "benchmark_verdict_good")
        self.assertEqual(_verdict(ok), "benchmark_verdict_ok")
        self.assertEqual(_verdict(slow), "benchmark_verdict_slow")

    def test_verdict_skips_unmeasured_metrics(self):
        partial = {"cpu_mops": 10.0, "ram_mbps": 0.0, "disk_write_mbps": 0.0, "disk_read_mbps": 3000.0}
        self.assertEqual(_verdict(partial), "benchmark_verdict_great")
        self.assertEqual(_verdict({"cpu_mops": 0.0}), "benchmark_verdict_ok")

    def test_run_table_mode_includes_verdict_and_explanation(self):
        from io import StringIO

        stream = StringIO()
        console = Console(file=stream, force_terminal=True, width=100)
        t = build_translator("en")
        rc = run(console, t)
        output = stream.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("What these numbers mean", output)
        self.assertIn("higher is better", output)
        # a verdict emoji is always rendered — which one depends on the host
        self.assertTrue(any(emoji in output for emoji in ("🟢", "🟡", "🔴")))

    def test_run_json_mode_has_no_verdict(self):
        """JSON output stays machine-pure: no verdict/explanation text."""
        import json as jsonlib
        from io import StringIO

        stream = StringIO()
        console = Console(file=stream, width=100)
        t = build_translator("en")
        rc = run(console, t, as_json=True)
        data = jsonlib.loads(stream.getvalue())
        self.assertEqual(rc, 0)
        self.assertEqual(
            set(data),
            {"cpu_mops", "ram_mbps", "disk_write_mbps", "disk_read_mbps", "elapsed_seconds"},
        )
        self.assertNotIn("🟢", stream.getvalue())

    def test_delta_pct(self):
        self.assertAlmostEqual(_delta_pct(120.0, 100.0), 20.0)
        self.assertAlmostEqual(_delta_pct(80.0, 100.0), -20.0)
        self.assertIsNone(_delta_pct(0.0, 100.0))
        self.assertIsNone(_delta_pct(100.0, 0.0))
        self.assertIsNone(_delta_pct(None, 100.0))

    def test_baseline_roundtrip(self):
        with tempfile.TemporaryDirectory() as base:
            self.assertTrue(save_baseline({"cpu_mops": 5.0}, base=base))
            loaded = load_baseline(base=base)
            self.assertEqual(loaded["results"]["cpu_mops"], 5.0)
            self.assertIn("timestamp", loaded)

    def test_load_baseline_missing_returns_empty(self):
        with tempfile.TemporaryDirectory() as base:
            self.assertEqual(load_baseline(base=base), {})

    def test_compare_first_run_creates_baseline_and_second_run_shows_delta(self):
        from io import StringIO

        t = build_translator("en")
        with tempfile.TemporaryDirectory() as base:
            # First run: no baseline yet -> friendly notice + baseline saved.
            first_stream = StringIO()
            console = Console(file=first_stream, force_terminal=True, width=100)
            rc = run(console, t, compare=True, base=base)
            first_output = first_stream.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("No previous benchmark found", first_output)
            self.assertIn("Baseline saved", first_output)

            # Second run: baseline exists -> delta column rendered.
            second_stream = StringIO()
            console = Console(file=second_stream, force_terminal=True, width=100)
            rc = run(console, t, compare=True, base=base)
            second_output = second_stream.getvalue()
            self.assertEqual(rc, 0)
            self.assertIn("Δ vs baseline", second_output)
            self.assertIn("Baseline from", second_output)
            self.assertIn("%", second_output)  # a delta percentage is shown

    def test_plain_run_does_not_write_baseline(self):
        from io import StringIO

        with tempfile.TemporaryDirectory() as base:
            stream = StringIO()
            console = Console(file=stream, force_terminal=True, width=100)
            rc = run(console, build_translator("en"), base=base)
            self.assertEqual(rc, 0)
            self.assertEqual(load_baseline(base=base), {})

    def test_json_mode_ignores_compare(self):
        """--benchmark --json stays machine-pure: no baseline file, no text."""
        import json as jsonlib
        from io import StringIO

        with tempfile.TemporaryDirectory() as base:
            stream = StringIO()
            console = Console(file=stream, width=100)
            rc = run(console, build_translator("en"), as_json=True, compare=True, base=base)
            data = jsonlib.loads(stream.getvalue())
            self.assertEqual(rc, 0)
            self.assertNotIn("Δ vs baseline", stream.getvalue())
            self.assertEqual(load_baseline(base=base), {})
            self.assertEqual(
                set(data),
                {"cpu_mops", "ram_mbps", "disk_write_mbps", "disk_read_mbps", "elapsed_seconds"},
            )

    def test_run_json_mode_stays_valid_on_narrow_console(self):
        """Smoke: benchmark JSON stays machine-parseable on a narrow
        80-column console. Benchmark values are short numbers, so this is a
        parseability guard; the hostile-value case (long strings / embedded
        newlines) is covered by the inspector regression test, where string
        values can be long and contain control characters.
        """
        import json as jsonlib
        from io import StringIO

        stream = StringIO()
        console = Console(file=stream, width=80)
        t = build_translator("en")
        rc = run(console, t, as_json=True)
        data = jsonlib.loads(stream.getvalue())
        self.assertEqual(rc, 0)
        self.assertEqual(
            set(data),
            {"cpu_mops", "ram_mbps", "disk_write_mbps", "disk_read_mbps", "elapsed_seconds"},
        )


if __name__ == "__main__":
    unittest.main()
