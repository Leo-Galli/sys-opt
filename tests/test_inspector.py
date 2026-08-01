# -*- coding: utf-8 -*-
"""Tests for the inspector: collection runs on the live host without crashing."""

import json
import unittest

from sys_opt.i18n.languages import build_translator
from sys_opt.inspector import collect, to_dict


class TestInspector(unittest.TestCase):
    def setUp(self):
        # NOTE: store the translator on the *instance* (not the class) so it
        # is a plain function and not bound as a method.
        self.t = build_translator("en")
        self.sections = collect(self.t)

    def test_collect_returns_all_sections(self):
        titles = [s["title"] for s in self.sections]
        for expected in (
            "Operating System",
            "Motherboard",
            "CPU",
            "Memory",
            "Graphics",
            "Storage",
        ):
            self.assertTrue(
                any(expected in title for title in titles),
                "missing section containing: %s (titles: %s)" % (expected, titles),
            )

    def test_kv_rows_are_non_empty_strings(self):
        for section in self.sections:
            if section["type"] == "kv":
                for key, value in section["rows"]:
                    self.assertIsInstance(value, str, "%s must be a string" % key)
                    self.assertTrue(value, "empty value for %s" % key)

    def test_table_sections_have_rows(self):
        for section in self.sections:
            if section["type"] == "table":
                self.assertTrue(section["headers"])
                self.assertIsInstance(section["rows"], list)

    def test_to_dict_is_json_serializable(self):
        payload = to_dict(self.t, self.sections)
        dumped = json.dumps(payload, ensure_ascii=False)
        self.assertIsInstance(dumped, str)
        self.assertGreater(len(dumped), 0)


if __name__ == "__main__":
    unittest.main()
