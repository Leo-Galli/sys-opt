# -*- coding: utf-8 -*-
"""Tests for the optimizer: step assembly, profiles and dry-run safety."""

import os
import unittest

from sys_opt.i18n.languages import build_translator
from sys_opt.optimizer import PROFILE_ORDER, build_steps


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


if __name__ == "__main__":
    unittest.main()
