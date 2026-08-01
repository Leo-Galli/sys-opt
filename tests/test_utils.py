# -*- coding: utf-8 -*-
"""Tests for shared utilities."""

import re
import tempfile
import unittest

from sys_opt.utils import (
    _display_width,
    _fit_width,
    _menu_frame,
    config_path,
    format_bytes,
    format_freq,
    format_uptime,
    is_admin,
    load_config,
    run_cmd,
    save_config,
)

_ANSI = re.compile(r"\x1b\[[0-9;]*m")


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


class TestArrowMenu(unittest.TestCase):
    """The archinstall-style boxed menu must never wrap (redraw math)."""

    def test_frame_is_boxed(self):
        frame = _menu_frame("Title", ["Alpha", "Beta"], 0, "hint", width=40)
        self.assertTrue(frame[0].startswith("\x1b[36m┌─"))
        self.assertTrue(frame[-1].endswith("┘\x1b[0m"))
        self.assertTrue(frame[-1].startswith("\x1b[36m└"))
        self.assertIn("─", frame[0])

    def test_selected_row_has_cursor_marker(self):
        frame = _menu_frame("T", ["Alpha", "Beta"], 0, None, width=40)
        selected = _ANSI.sub("", frame[2])
        other = _ANSI.sub("", frame[3])
        self.assertIn("▸ 1. Alpha", selected)
        self.assertIn("  2. Beta", other)
        self.assertNotIn("▸", other)

    def test_cursor_moves_to_other_row(self):
        frame = _menu_frame("T", ["Alpha", "Beta"], 1, None, width=40)
        first = _ANSI.sub("", frame[2])
        second = _ANSI.sub("", frame[3])
        self.assertIn("  1. Alpha", first)
        self.assertIn("▸ 2. Beta", second)

    def test_rows_never_wrap_wide_chars(self):
        """Even with emoji/CJK items every line fits the width exactly."""
        frame = _menu_frame(
            "Menu", ["🔍 Inspect", "日本語の項目が長い場合", "🚀 Optimize"], 1, "Use ↑/↓", width=40
        )
        for line in frame:
            visible = _ANSI.sub("", line)
            self.assertLessEqual(_display_width(visible), 40, repr(visible))

    def test_frame_height_is_constant(self):
        """Redraw math moves up len(frame) lines; height must not change."""
        first = _menu_frame("T", ["A", "B", "C"], 0, "hint", width=40)
        second = _menu_frame("T", ["A", "B", "C"], 2, "hint", width=40)
        self.assertEqual(len(first), len(second))
        self.assertEqual(len(first), 8)  # border + blank + 3 items + blank + hint + border

    def test_fit_width_respects_display_columns(self):
        self.assertEqual(_display_width("abc"), 3)
        self.assertEqual(_display_width("🔍"), 2)
        self.assertLessEqual(_display_width(_fit_width("日本語です", 6)), 6)
        self.assertEqual(_fit_width("abc", 2), "ab")


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
