# -*- coding: utf-8 -*-
"""Tests for the optimizer: step assembly, profiles and dry-run safety."""

import io
import os
import unittest
from unittest import mock

from rich.console import Console

from sys_opt.i18n.languages import build_translator
from sys_opt.optimizer import PROFILE_ORDER, build_steps, _parse_apply_selection, _step_impact


def _string_console():
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=False, width=100)
    return buffer, console


class TestOptimizer(unittest.TestCase):
    def test_build_steps_returns_non_empty_list(self):
        t = build_translator("en")
        steps = build_steps(t, elevated=False, dry_run=True)
        self.assertIsInstance(steps, list)
        self.assertGreater(len(steps), 0)
        for label, fn in steps:
            self.assertIsInstance(label, str)
            self.assertTrue(label)
            self.assertTrue(callable(fn))

    def test_every_profile_has_steps(self):
        t = build_translator("en")
        self.assertIn("all", PROFILE_ORDER)
        for profile in PROFILE_ORDER:
            steps = build_steps(t, elevated=False, dry_run=True, profile=profile)
            self.assertGreater(len(steps), 0, "profile '%s' has no steps" % profile)

    def test_profile_filters_windows_steps(self):
        if os.name != "nt":
            self.skipTest("Windows-only assertions")
        from sys_opt.optimizer import (
            _step_win_gpu_sched,
            _step_win_game_dvr,
            _step_win_power,
        )

        t = build_translator("en")
        clean_fns = [fn for _, fn in build_steps(t, True, True, "clean")]
        gaming_fns = [fn for _, fn in build_steps(t, True, True, "gaming")]
        all_fns = [fn for _, fn in build_steps(t, True, True, "all")]
        self.assertNotIn(_step_win_gpu_sched, clean_fns)
        self.assertNotIn(_step_win_game_dvr, clean_fns)
        self.assertNotIn(_step_win_power, clean_fns)
        self.assertIn(_step_win_gpu_sched, gaming_fns)
        self.assertIn(_step_win_game_dvr, gaming_fns)
        self.assertIn(_step_win_gpu_sched, all_fns)
        self.assertIn(_step_win_power, all_fns)

    def test_steps_run_safely_in_dry_run(self):
        t = build_translator("en")
        steps = build_steps(t, elevated=True, dry_run=True)
        for _label, fn in steps:
            try:
                status, detail = fn(t, elevated=True, dry_run=True)
            except Exception as exc:  # zero-crash policy
                self.fail("step raised: %s" % exc)
            self.assertIn(status, ("ok", "failed", "skipped", "skipped_no_elev"))
            self.assertIsInstance(detail, str)

    def test_suggest_dry_run_returns_zero_and_shows_table(self):
        """--optimize --suggest --dry-run must show the ranked table and change nothing."""
        from sys_opt.optimizer import suggest

        t = build_translator("en")
        buffer, console = _string_console()
        code = suggest(console, t, profile="gaming", dry_run=True)
        out = buffer.getvalue()
        self.assertEqual(code, 0)
        self.assertIn(t("suggest_header"), out)
        self.assertIn(t("suggest_col_impact"), out)
        self.assertIn(t("suggest_dry_run_note"), out)

    def test_suggest_dry_run_never_executes_steps(self):
        """In dry-run mode no step may run, even for 'ready' states."""
        from sys_opt.optimizer import suggest

        t = build_translator("en")
        calls = []

        def fake_step(_t, _elevated, _dry_run):
            calls.append("step-called")
            return "ok", "detail"

        with mock.patch("sys_opt.optimizer.build_steps", return_value=[("fake", fake_step)]):
            with mock.patch(
                "sys_opt.optimizer._DETECT_STEPS", {fake_step: lambda _e: ("ready", "")}
            ):
                buffer, console = _string_console()
                code = suggest(console, t, dry_run=True)
        self.assertEqual(code, 0)
        self.assertEqual(calls, [])

    def test_suggest_all_applied_shows_nothing_to_do(self):
        from sys_opt.optimizer import suggest

        t = build_translator("en")

        def fake_step(_t, _elevated, _dry_run):
            return "ok", "detail"

        with mock.patch("sys_opt.optimizer.build_steps", return_value=[("fake", fake_step)]):
            with mock.patch(
                "sys_opt.optimizer._DETECT_STEPS", {fake_step: lambda _e: ("applied", "0 files")}
            ):
                buffer, console = _string_console()
                code = suggest(console, t)
        self.assertEqual(code, 0)
        self.assertIn(t("suggest_nothing"), buffer.getvalue())

    def test_suggest_aborts_when_no_confirmation(self):
        """Without a positive confirmation (default 'none'), nothing is applied."""
        from sys_opt.optimizer import suggest

        t = build_translator("en")
        calls = []

        def fake_step(_t, _elevated, _dry_run):
            calls.append("step-called")
            return "ok", "detail"

        with mock.patch("sys_opt.optimizer.build_steps", return_value=[("fake", fake_step)]):
            with mock.patch(
                "sys_opt.optimizer._DETECT_STEPS", {fake_step: lambda _e: ("ready", "")}
            ):
                with mock.patch("sys_opt.optimizer.is_admin", return_value=True):
                    with mock.patch("rich.prompt.Prompt.ask", return_value="none"):
                        buffer, console = _string_console()
                        code = suggest(console, t)
        self.assertEqual(code, 0)
        self.assertEqual(calls, [])
        self.assertIn(t("suggest_abort"), buffer.getvalue())

    def test_suggest_applies_only_confirmed_steps(self):
        """'all' confirmation runs the ready steps; non-actionable ones stay out."""
        from sys_opt.optimizer import suggest

        t = build_translator("en")
        calls = []

        def fake_step(_t, _elevated, _dry_run):
            calls.append("fake")
            return "ok", "detail"

        def other_step(_t, _elevated, _dry_run):
            calls.append("other")
            return "ok", "detail"

        with mock.patch(
            "sys_opt.optimizer.build_steps", return_value=[("fake", fake_step), ("other", other_step)]
        ):
            with mock.patch(
                "sys_opt.optimizer._DETECT_STEPS",
                {fake_step: lambda _e: ("ready", ""), other_step: lambda _e: ("applied", "")},
            ):
                with mock.patch("sys_opt.optimizer.is_admin", return_value=True):
                    with mock.patch("rich.prompt.Prompt.ask", return_value="all"):
                        buffer, console = _string_console()
                        code = suggest(console, t)
        self.assertEqual(code, 0)
        self.assertEqual(calls, ["fake"])  # only the ready step ran
        self.assertIn(t("suggest_applying"), buffer.getvalue())

    def test_suggest_apply_selection_parsing(self):
        rows = [
            {"_num": 1, "status": "ready"},
            {"_num": 2, "status": "needs_elevation"},
            {"_num": 3, "status": "ready"},
            {"_num": None, "status": "applied"},
            {"_num": None, "status": "not_applicable"},
        ]
        self.assertEqual([r["_num"] for r in _parse_apply_selection("all", rows)], [1, 2, 3])
        self.assertEqual(_parse_apply_selection("none", rows), [])
        self.assertEqual(_parse_apply_selection("", rows), [])
        self.assertEqual([r["_num"] for r in _parse_apply_selection("1,3", rows)], [1, 3])
        self.assertEqual([r["_num"] for r in _parse_apply_selection("2 3", rows)], [2, 3])
        # numbered non-actionable rows are ignored, as are out-of-range / junk tokens
        self.assertEqual(_parse_apply_selection("4", rows), [])
        self.assertEqual(
            [r["_num"] for r in _parse_apply_selection("1,99,abc", rows)], [1]
        )

    def test_suggest_impact_is_ranked_by_profile(self):
        """The gaming profile must rate FPS-critical steps above cleanup-only ones."""
        from sys_opt.optimizer import (
            _step_win_gpu_sched,
            _step_win_game_dvr,
            _step_win_temp,
        )

        if os.name != "nt":
            self.skipTest("Windows-only impact assertions")
        self.assertGreater(_step_impact(_step_win_gpu_sched, "gaming"), _step_impact(_step_win_temp, "gaming"))
        self.assertEqual(_step_impact(_step_win_gpu_sched, "gaming"), 5)
        self.assertEqual(_step_impact(_step_win_game_dvr, "gaming"), 5)
        self.assertGreaterEqual(_step_impact(_step_win_temp, "clean"), _step_impact(_step_win_temp, "gaming"))

    def test_all_steps_have_detector_impact_and_why(self):
        """Every step of every profile must carry a detector, impact and reason key."""
        from sys_opt.optimizer import _DETECT_STEPS, _STEP_IMPACT, _STEP_WHY, _steps_for_os

        t = build_translator("en")
        steps = [fn for _label, fn in _steps_for_os(t)]
        self.assertTrue(steps)
        for fn in steps:
            self.assertIn(fn, _DETECT_STEPS, "no detector for %s" % fn.__name__)
            self.assertIn(fn, _STEP_IMPACT, "no impact map for %s" % fn.__name__)
            self.assertIn(fn, _STEP_WHY, "no why-key for %s" % fn.__name__)
        for profile in PROFILE_ORDER:
            for fn in steps:
                stars = _step_impact(fn, profile)
                self.assertGreaterEqual(stars, 1)
                self.assertLessEqual(stars, 5)

    def test_detectors_return_valid_statuses_without_crashing(self):
        """Detectors are read-only and must never raise on the host OS."""
        from sys_opt.optimizer import _DETECT_STEPS, _steps_for_os

        t = build_translator("en")
        steps = [fn for _label, fn in _steps_for_os(t)]
        for fn in steps:
            try:
                status, _detail = _DETECT_STEPS[fn](elevated=False)
            except Exception as exc:  # zero-crash policy
                self.fail("detector %s raised: %s" % (fn.__name__, exc))
            self.assertIn(status, ("ready", "applied", "needs_elevation", "not_applicable"))

    def test_classify_result_buckets(self):
        """The summary bucket logic covers every status x detected combination."""
        from sys_opt.optimizer import _classify_result

        cases = [
            # (status, detected, expected bucket)
            ("ok", "ready", "applied"),
            ("ok", "needs_elevation", "applied"),
            ("ok", "applied", "already"),
            ("ok", "not_applicable", "unsupported"),
            ("skipped", "applied", "already"),
            ("skipped", "not_applicable", "unsupported"),
            ("skipped", "needs_elevation", "needs_elevation"),
            ("skipped", "ready", "skipped"),
            ("skipped_no_elev", "ready", "needs_elevation"),
            ("skipped_no_elev", "applied", "already"),
            ("failed", "ready", "failed"),
            # failed always wins: a red FAILED is never hidden under "already"
            ("failed", "applied", "failed"),
            ("failed", "not_applicable", "failed"),
        ]
        for status, detected, expected in cases:
            self.assertEqual(
                _classify_result(status, detected), expected,
                "(%s, %s) should be %s" % (status, detected, expected),
            )

    def test_final_summary_verdict_and_buckets(self):
        """--optimize must end with a verdict panel: applied vs skipped + reason."""
        from sys_opt.optimizer import run

        t = build_translator("en")
        calls = []

        def ok_step(_t, _elevated, _dry_run):
            calls.append("ok")
            return "ok", "detail"

        def fail_step(_t, _elevated, _dry_run):
            calls.append("fail")
            return "failed", "detail"

        def elev_step(_t, _elevated, _dry_run):
            calls.append("elev")
            return "skipped_no_elev", "detail"

        steps = [("one", ok_step), ("two", fail_step), ("three", elev_step)]
        with mock.patch("sys_opt.optimizer.build_steps", return_value=steps):
            with mock.patch(
                "sys_opt.optimizer._DETECT_STEPS",
                {
                    ok_step: lambda _e: ("ready", ""),
                    fail_step: lambda _e: ("ready", ""),
                    elev_step: lambda _e: ("ready", ""),
                },
            ):
                with mock.patch("sys_opt.optimizer.is_admin", return_value=True):
                    buffer, console = _string_console()
                    code = run(console, t, dry_run=False)
        out = buffer.getvalue()
        self.assertEqual(code, 1)  # one failed step
        self.assertEqual(sorted(calls), ["elev", "fail", "ok"])
        # verdict counts the 3 actionable steps, 1 applied
        self.assertIn("1 of 3 possible optimizations applied", out)
        self.assertIn(t("summary_applied"), out)
        self.assertIn(t("summary_failed"), out)
        self.assertIn(t("summary_needs_elevation"), out)

    def test_final_summary_nothing_to_do(self):
        """When every step is already applied, the verdict says nothing to do."""
        from sys_opt.optimizer import run

        t = build_translator("en")

        def ok_step(_t, _elevated, _dry_run):
            return "ok", "detail"

        with mock.patch("sys_opt.optimizer.build_steps", return_value=[("one", ok_step)]):
            with mock.patch(
                "sys_opt.optimizer._DETECT_STEPS", {ok_step: lambda _e: ("applied", "0 files")}
            ):
                with mock.patch("sys_opt.optimizer.is_admin", return_value=True):
                    buffer, console = _string_console()
                    code = run(console, t, dry_run=False)
        out = buffer.getvalue()
        self.assertEqual(code, 0)
        self.assertIn(t("summary_nothing"), out)
        # the 'nothing to do' panel replaces the verdict line entirely
        self.assertNotIn("possible optimizations applied", out)

    def test_final_summary_verdict_string_has_two_placeholders(self):
        """Every language's summary_verdict must carry exactly two %d slots."""
        from sys_opt.i18n.languages import LANGUAGES

        for code, meta in LANGUAGES.items():
            value = meta["strings"]["summary_verdict"]
            self.assertEqual(
                value.count("%d"), 2,
                "[%s] summary_verdict must have 2 placeholders: %r" % (code, value),
            )


if __name__ == "__main__":
    unittest.main()
