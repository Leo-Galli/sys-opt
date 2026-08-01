# -*- coding: utf-8 -*-
"""Tests for shared utilities."""

import tempfile
import unittest

from sys_opt.utils import (
    config_path,
    format_bytes,
    format_freq,
    format_uptime,
    is_admin,
    load_config,
    run_cmd,
    save_config,
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


class TestConfigPersistence(unittest.TestCase):
    """The user's language choice must survive across launches."""

    def test_save_then_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as base:
            self.assertTrue(save_config("ja", base=base))
            loaded = load_config(base=base)
            self.assertEqual(loaded.get("language"), "ja")
            self.assertTrue(config_path(base).exists())

    def test_load_config_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as base:
            self.assertEqual(load_config(base=base), {})

    def test_save_config_updates_instead_of_overwriting(self):
        with tempfile.TemporaryDirectory() as base:
            save_config("it", base=base)
            save_config("fr", base=base)
            loaded = load_config(base=base)
            self.assertEqual(loaded.get("language"), "fr")

    def test_save_config_never_raises_on_bad_base(self):
        import os

        # A base that is an existing *file* cannot be mkdir'd → returns False
        # (portable across Windows/macOS/Linux, where a rooted bogus path may
        # actually resolve to a creatable directory on the current drive).
        with tempfile.TemporaryDirectory() as base:
            blocker = os.path.join(base, "blocker")
            with open(blocker, "w", encoding="utf-8") as handle:
                handle.write("x")
            self.assertFalse(save_config("en", base=blocker))


def sys_executable():
    import sys

    return sys.executable


if __name__ == "__main__":
    unittest.main()
