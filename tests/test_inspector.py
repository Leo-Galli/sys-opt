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

    def test_json_output_stays_valid_with_hostile_values(self):
        """Regression: rich's JSON renderable and the 80-column wrapping used
        to re-emit raw control characters / split long values, producing
        invalid JSON when piped (seen on macOS, where sysctl CPU values end
        with a newline and exceed 80 columns). The output must stay parseable
        and round-trip the hostile value intact.
        """
        import json as jsonlib
        from io import StringIO

        from rich.console import Console

        from sys_opt import inspector

        nasty_model = "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz" + " X" * 30 + "\n"
        original = inspector._cpu_model
        inspector._cpu_model = lambda: nasty_model
        try:
            stream = StringIO()
            console = Console(file=stream, width=80)
            inspector.run(console, self.t, as_json=True)
            data = jsonlib.loads(stream.getvalue())
        finally:
            inspector._cpu_model = original
        self.assertEqual(data["CPU"]["Model"], nasty_model)


if __name__ == "__main__":
    unittest.main()
