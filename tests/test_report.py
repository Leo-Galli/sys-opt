# -*- coding: utf-8 -*-
"""Tests for the HTML performance report module (--report)."""

import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

from rich.console import Console

from sys_opt import report
from sys_opt.i18n.languages import LANGUAGES, build_translator


class TestReport(unittest.TestCase):
    def test_build_html_contains_specs(self):
        t = build_translator("en")
        sections = [
            {"type": "kv", "title": "OS", "rows": [("label_os", "Windows 11")]},
            {"type": "table", "title": "GPU", "headers": ["Name"], "rows": [["RTX 4090"]]},
        ]
        page = report.build_html(t, language="en", sections=sections)
        self.assertIn("Performance Report", page)
        self.assertIn("Windows 11", page)
        self.assertIn("RTX 4090", page)

    def test_build_html_contains_benchmark_before_after(self):
        t = build_translator("en")
        before = {
            "cpu_mops": 1.0, "ram_mbps": 5000.0,
            "disk_write_mbps": 200.0, "disk_read_mbps": 300.0,
        }
        after = {
            "cpu_mops": 2.0, "ram_mbps": 6000.0,
            "disk_write_mbps": 250.0, "disk_read_mbps": 350.0,
        }
        page = report.build_html(t, language="en", before=before, after=after, sections=[])
        self.assertIn("Before", page)
        self.assertIn("After", page)
        self.assertIn("1.00 M ops/s", page)
        self.assertIn("2.00 M ops/s", page)
        self.assertIn("+100.0%", page)  # CPU doubled

    def test_build_html_escapes_values(self):
        t = build_translator("en")
        sections = [
            {"type": "kv", "title": "Evil", "rows": [("label_os", "<script>alert(1)</script>")]}
        ]
        page = report.build_html(t, language="en", sections=sections)
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_write_report_creates_file(self):
        t = build_translator("en")
        with tempfile.TemporaryDirectory() as base:
            path = report.write_report(t, base=base)
            self.assertIsNotNone(path)
            self.assertTrue(Path(path).exists())
            self.assertIn("<html", Path(path).read_text(encoding="utf-8"))

    def test_open_report_uses_browser(self):
        t = build_translator("en")
        with tempfile.TemporaryDirectory() as base:
            path = report.write_report(t, base=base)
            with mock.patch("sys_opt.report.webbrowser.open", return_value=True) as mocked:
                self.assertTrue(report.open_report(path))
            mocked.assert_called_once()

    def test_run_benchmark_report_writes_report(self):
        t = build_translator("en")
        stream = StringIO()
        console = Console(file=stream, width=100)
        with tempfile.TemporaryDirectory() as base:
            with mock.patch("sys_opt.report.webbrowser.open", return_value=True):
                rc = report.run_benchmark_report(console, t, base=base)
            self.assertEqual(rc, 0)
            output = stream.getvalue()
            self.assertIn("Report saved", output)
            reports = Path(base) / "reports"
            self.assertTrue(any(reports.glob("*.html")))

    def test_run_optimize_report_flow(self):
        t = build_translator("en")
        stream = StringIO()
        console = Console(file=stream, width=100)
        with tempfile.TemporaryDirectory() as base:
            with mock.patch("sys_opt.report.webbrowser.open", return_value=True), \
                    mock.patch("sys_opt.optimizer.run", return_value=0):
                rc = report.run_optimize_report(console, t, dry_run=True, base=base)
            self.assertEqual(rc, 0)
            output = stream.getvalue()
            self.assertIn("Baseline (before) saved", output)
            self.assertIn("After result saved", output)
            self.assertIn("Report saved", output)

    def test_report_placeholder_keys_all_languages(self):
        """Placeholder-bearing keys must keep exactly one placeholder."""
        for code, meta in LANGUAGES.items():
            self.assertEqual(meta["strings"]["report_path"].count("%s"), 1, code)
            self.assertEqual(meta["strings"]["filebench_too_large"].count("%d"), 1, code)
            self.assertEqual(meta["strings"]["filebench_port_busy"].count("%d"), 1, code)


if __name__ == "__main__":
    unittest.main()
