# -*- coding: utf-8 -*-
"""
Function-level CLI smoke tests — the safety net for every main flag.

Each test runs the real ``sys_opt.main.main(argv)`` end-to-end (argument
parsing → console → runner) with the output captured, and asserts the exit
code plus the presence of the expected rendered sections. Because this file
lives in ``tests/``, the CI matrix executes it on every OS (Windows, macOS,
Linux, incl. arm64) × Python 3.8–3.14 combination — proving the CLI entry
points and their rendering work everywhere, not just on the dev machine.

Design notes:
- ``--language en`` forces deterministic English labels on every OS.
- A StringIO-backed rich Console is injected so rendering is captured
  without needing a TTY; argparse's ``--version`` (which exits via
  SystemExit) is translated to an exit code.
- Nothing here requires elevation: ``--optimize`` always uses ``--dry-run``.
"""

import contextlib
import io
import json
import unittest
from unittest import mock

from rich.console import Console

from sys_opt.main import main


def run_cli(argv, width=100):
    """Run the CLI in-process; returns (exit_code, captured_output).

    Redirects stdout (argparse writes ``--version`` there) and injects a
    StringIO-backed rich Console so all table/panel rendering is captured
    too. Never raises: argparse exits via SystemExit for ``--version`` and
    parse errors, which is translated into an exit code.
    """
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=False, width=width)
    with mock.patch("sys_opt.main._make_console", return_value=console):
        with contextlib.redirect_stdout(buffer):
            try:
                code = main(argv)
            except SystemExit as exc:  # argparse --version / parse errors
                code = exc.code if isinstance(exc.code, int) else 0
    return code, buffer.getvalue()


class TestCliSmoke(unittest.TestCase):
    """Every main CLI flag runs end-to-end and renders expected output."""

    def test_version_flag(self):
        code, output = run_cli(["--version"])
        self.assertEqual(code, 0)
        self.assertIn("sys-opt", output)

    def test_list_languages_flag(self):
        code, output = run_cli(["--list-languages"])
        self.assertEqual(code, 0)
        for label in ("English", "Italiano", "日本語", "العربية"):
            self.assertIn(label, output)

    def test_inspect_renders_table(self):
        code, output = run_cli(["--inspect", "--language", "en"])
        self.assertEqual(code, 0)
        self.assertIn("System Inspection", output)
        self.assertIn("Operating System & Kernel", output)
        self.assertIn("CPU", output)

    def test_inspect_json_is_valid(self):
        code, output = run_cli(["--inspect", "--json", "--language", "en"])
        self.assertEqual(code, 0)
        data = json.loads(output)
        self.assertIn("Operating System & Kernel", data)

    def test_optimize_dry_run(self):
        code, output = run_cli(["--optimize", "--dry-run", "--language", "en"])
        self.assertEqual(code, 0)
        self.assertIn("System Optimization", output)
        self.assertIn("dry-run", output)

    def test_optimize_dry_run_gaming_profile(self):
        code, output = run_cli(
            ["--optimize", "--dry-run", "--profile", "gaming", "--language", "en"]
        )
        self.assertEqual(code, 0)
        self.assertIn("Gaming", output)

    def test_optimize_suggest_dry_run(self):
        code, output = run_cli(
            ["--optimize", "--suggest", "--dry-run", "--profile", "gaming", "--language", "en"]
        )
        self.assertEqual(code, 0)
        self.assertIn("Optimization Suggestions", output)
        self.assertIn("Impact", output)
        self.assertIn("Suggestion mode", output)

    def test_benchmark_renders_table(self):
        code, output = run_cli(["--benchmark", "--language", "en"])
        self.assertEqual(code, 0)
        self.assertIn("Performance Benchmark", output)
        self.assertIn("MB/s", output)

    def test_benchmark_json_is_valid(self):
        code, output = run_cli(["--benchmark", "--json", "--language", "en"])
        self.assertEqual(code, 0)
        data = json.loads(output)
        for key in ("cpu_mops", "ram_mbps", "disk_write_mbps", "disk_read_mbps"):
            self.assertIn(key, data)

    def test_unsupported_language_flag_falls_back(self):
        """An unknown --language must not crash; it detects/falls back.

        The assertion is language-independent on purpose: the CPU section
        title contains "CPU" in all 10 languages (e.g. "Процессор (CPU)",
        "中央处理器 (CPU)"), so this holds whether the fallback lands on a
        saved config, the detected locale or English.
        """
        code, output = run_cli(["--inspect", "--language", "xx"])
        self.assertEqual(code, 0)
        self.assertIn("CPU", output)


if __name__ == "__main__":
    unittest.main()
