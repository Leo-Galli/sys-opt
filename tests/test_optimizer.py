# -*- coding: utf-8 -*-
"""Tests for the optimizer: step assembly and dry-run safety."""

import unittest

from sys_opt.i18n.languages import build_translator
from sys_opt.optimizer import build_steps, run


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
