# -*- coding: utf-8 -*-
"""Tests for the self-update module (PyPI check, prompt, install)."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from rich.console import Console

from sys_opt import __version__
from sys_opt.update import (
    install_update,
    latest_pypi_version,
    maybe_prompt,
    needs_update,
    run_update_cli,
    version_key,
)


def _console():
    return Console(file=io.StringIO(), force_terminal=False, width=100)


def _patch_config(base):
    """Redirect the update module's config paths to a temp dir (both are
    needed: config_dir for the mkdir, config_path for the file itself)."""
    return [
        mock.patch("sys_opt.update.config_path", return_value=Path(base) / "config.json"),
        mock.patch("sys_opt.update.config_dir", return_value=Path(base)),
    ]


class _FakeResponse:
    """Minimal context-manager HTTP response for urlopen mocking."""

    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self._payload


class TestVersionCompare(unittest.TestCase):
    def test_version_key_parses_dotted(self):
        self.assertEqual(version_key("1.2.3"), (1, 2, 3))

    def test_version_key_ignores_prerelease_suffix(self):
        self.assertEqual(version_key("1.10rc2"), (1, 10, 0))
        self.assertEqual(version_key("2.0.0b1"), (2, 0, 0))

    def test_version_key_garbage_is_safe(self):
        self.assertEqual(version_key("garbage"), (0, 0, 0))
        self.assertEqual(version_key(None), (0, 0, 0))
        self.assertEqual(version_key(""), (0, 0, 0))

    def test_needs_update_true_for_newer(self):
        self.assertTrue(needs_update("9.9.9", current="1.0.0"))

    def test_needs_update_false_when_equal_or_older(self):
        self.assertFalse(needs_update("1.0.0", current="1.0.0"))
        self.assertFalse(needs_update("0.9.0", current="1.0.0"))

    def test_needs_update_garbage_never_raises(self):
        self.assertFalse(needs_update("not-a-version", current="1.0.0"))


class TestPyPiCheck(unittest.TestCase):
    def test_latest_pypi_version_parses_payload(self):
        payload = json.dumps({"info": {"version": "2.3.4"}}).encode("utf-8")
        with mock.patch(
            "sys_opt.update.urllib.request.urlopen",
            return_value=_FakeResponse(payload),
        ):
            self.assertEqual(latest_pypi_version(), "2.3.4")

    def test_latest_pypi_version_zero_crash_on_network_error(self):
        with mock.patch(
            "sys_opt.update.urllib.request.urlopen",
            side_effect=OSError("no network"),
        ):
            self.assertIsNone(latest_pypi_version())

    def test_latest_pypi_version_zero_crash_on_bad_json(self):
        with mock.patch(
            "sys_opt.update.urllib.request.urlopen",
            return_value=_FakeResponse(b"<html>not json"),
        ):
            self.assertIsNone(latest_pypi_version())


class TestInstallUpdate(unittest.TestCase):
    def test_install_success_prints_version(self):
        console = _console()
        with mock.patch("sys_opt.update.run_cmd", return_value=(0, "", "")):
            code = install_update(console, _console_translator(), "2.0.0")
        self.assertEqual(code, 0)
        self.assertIn("Updated to 2.0.0", console.file.getvalue())

    def test_install_failure_prints_manual_command(self):
        console = _console()
        with mock.patch("sys_opt.update.run_cmd", return_value=(1, "", "error")):
            code = install_update(console, _console_translator(), "2.0.0")
        self.assertEqual(code, 1)
        output = console.file.getvalue()
        self.assertIn("Update failed", output)
        self.assertIn("pip install --upgrade sys-opt", output)

    def test_install_uses_python_m_pip(self):
        with mock.patch("sys_opt.update.run_cmd", return_value=(0, "", "")) as mocked:
            install_update(_console(), _console_translator(), "2.0.0")
        args = mocked.call_args[0][0]
        self.assertIn("-m", args)
        self.assertIn("pip", args)
        self.assertIn("--upgrade", args)
        self.assertIn("sys-opt", args)


class TestRunUpdateCli(unittest.TestCase):
    def test_up_to_date_exits_zero(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value=__version__):
            with _patch_config(base)[0], _patch_config(base)[1]:
                console = _console()
                code = run_update_cli(console, _console_translator())
        self.assertEqual(code, 0)
        self.assertIn("up to date", console.file.getvalue())

    def test_newer_version_triggers_install(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value="99.0.0"), \
                mock.patch("sys_opt.update.run_cmd", return_value=(0, "", "")):
            with _patch_config(base)[0], _patch_config(base)[1]:
                console = _console()
                code = run_update_cli(console, _console_translator())
        self.assertEqual(code, 0)
        output = console.file.getvalue()
        self.assertIn("99.0.0", output)
        self.assertIn("Updated to 99.0.0", output)

    def test_unreachable_exits_one(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value=None):
            with _patch_config(base)[0], _patch_config(base)[1]:
                console = _console()
                code = run_update_cli(console, _console_translator())
        self.assertEqual(code, 1)
        self.assertIn("Could not check for updates", console.file.getvalue())


class TestMaybePrompt(unittest.TestCase):
    def test_no_prompt_when_up_to_date(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value=__version__), \
                mock.patch("sys_opt.update.arrow_menu",
                           side_effect=AssertionError("must not prompt")):
            with _patch_config(base)[0], _patch_config(base)[1]:
                maybe_prompt(_console(), _console_translator(), base=base)

    def test_prompt_skipped_writes_skipped_version(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value="7.7.7"), \
                mock.patch("sys_opt.update.arrow_menu", return_value=1):
            with _patch_config(base)[0], _patch_config(base)[1]:
                maybe_prompt(_console(), _console_translator(), base=base)
            config = json.loads((Path(base) / "config.json").read_text(encoding="utf-8"))
            self.assertEqual(config.get("update_skipped"), "7.7.7")

    def test_skipped_version_is_not_asked_again(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value="7.7.7"), \
                mock.patch("sys_opt.update.arrow_menu",
                           side_effect=AssertionError("must not re-ask")):
            with _patch_config(base)[0], _patch_config(base)[1]:
                (Path(base) / "config.json").write_text(
                    json.dumps({"update_skipped": "7.7.7"}), encoding="utf-8"
                )
                maybe_prompt(_console(), _console_translator(), base=base)

    def test_confirm_runs_install(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value="7.7.7"), \
                mock.patch("sys_opt.update.arrow_menu", return_value=0), \
                mock.patch("sys_opt.update.run_cmd", return_value=(0, "", "")):
            with _patch_config(base)[0], _patch_config(base)[1]:
                console = _console()
                maybe_prompt(console, _console_translator(), base=base)
            self.assertIn("Updated to 7.7.7", console.file.getvalue())

    def test_offline_is_silent_and_does_not_write(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value=None), \
                mock.patch("sys_opt.update.arrow_menu",
                           side_effect=AssertionError("must not prompt")):
            with _patch_config(base)[0], _patch_config(base)[1]:
                console = _console()
                maybe_prompt(console, _console_translator(), base=base)
            self.assertEqual(console.file.getvalue(), "")
            self.assertFalse((Path(base) / "config.json").exists())

    def test_daily_cache_skips_network(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           side_effect=AssertionError("must not hit network")):
            with _patch_config(base)[0], _patch_config(base)[1]:
                # A check performed seconds ago → cached, no network call.
                cfg_path = Path(base) / "config.json"
                cfg_path.write_text(
                    json.dumps({"last_update_check": _now_seconds()}), encoding="utf-8"
                )
                maybe_prompt(_console(), _console_translator(), base=base)

    def test_daily_cache_records_after_successful_check(self):
        with tempfile.TemporaryDirectory() as base, \
                mock.patch("sys_opt.update.latest_pypi_version",
                           return_value=__version__):
            with _patch_config(base)[0], _patch_config(base)[1]:
                maybe_prompt(_console(), _console_translator(), base=base)
            config = json.loads((Path(base) / "config.json").read_text(encoding="utf-8"))
            self.assertIn("last_update_check", config)


def _now_seconds():
    import time

    return int(time.time())


def _console_translator():
    from sys_opt.i18n.languages import build_translator

    return build_translator("en")


if __name__ == "__main__":
    unittest.main()
