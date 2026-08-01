# -*- coding: utf-8 -*-
"""Tests for shared utilities."""

import unittest

from sys_opt.utils import (
    format_bytes,
    format_freq,
    format_uptime,
    is_admin,
    run_cmd,
)


class TestFormatting(unittest.TestCase):
    def test_format_bytes(self):
        self.assertEqual(format_bytes(512), "512 B")
        self.assertEqual(format_bytes(1536), "1.50 KiB")
        self.assertEqual(format_bytes(1073741824), "1.00 GiB")
        self.assertEqual(format_bytes(None), "N/A")
        self.assertEqual(format_bytes(-1), "N/A")
        self.assertEqual(format_bytes("garbage"), "N/A")

    def test_format_freq(self):
        self.assertEqual(format_freq(3.5e9), "3.50 GHz")
        self.assertEqual(format_freq(800e6), "800 MHz")
        self.assertEqual(format_freq(0), "N/A")
        self.assertEqual(format_freq(None), "N/A")

    def test_format_uptime(self):
        self.assertEqual(format_uptime(93784), "1d 2h 3m 4s")
        self.assertEqual(format_uptime(0), "0s")
        self.assertEqual(format_uptime(None), "N/A")


class TestSubprocess(unittest.TestCase):
    def test_run_cmd_missing_command_never_raises(self):
        code, _out, _err = run_cmd(["this-command-does-not-exist-xyz-123"])
        self.assertEqual(code, -1)

    def test_run_cmd_valid_command(self):
        code, out, _err = run_cmd([sys_executable(), "-c", "print('hello')"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "hello")


class TestElevation(unittest.TestCase):
    def test_is_admin_returns_bool(self):
        self.assertIsInstance(is_admin(), bool)


def sys_executable():
    import sys

    return sys.executable


if __name__ == "__main__":
    unittest.main()
