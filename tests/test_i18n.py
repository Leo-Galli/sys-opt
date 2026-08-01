# -*- coding: utf-8 -*-
"""Tests for the i18n engine: zero-missing-keys guarantee, fallback, detection."""

import unittest

from sys_opt.i18n.languages import (
    LANGUAGE_ORDER,
    LANGUAGES,
    build_translator,
    detect_system_language,
    validate_languages,
)


class TestI18n(unittest.TestCase):
    def test_ten_supported_languages(self):
        self.assertGreaterEqual(len(LANGUAGE_ORDER), 10)
        for code in ("it", "en", "es", "fr", "de", "pt", "ru", "zh", "ja", "ar"):
            self.assertIn(code, LANGUAGE_ORDER)

    def test_all_languages_have_identical_keys(self):
        issues = validate_languages()
        self.assertEqual(issues, [], "i18n issues found: %s" % issues)

    def test_every_language_has_meta(self):
        for code in LANGUAGE_ORDER:
            meta = LANGUAGES[code]
            for field in ("name", "native", "flag", "dir", "strings"):
                self.assertIn(field, meta, "%s missing meta field %s" % (code, field))

    def test_translator_returns_non_empty(self):
        t = build_translator("en")
        for key in LANGUAGES["en"]["strings"]:
            self.assertTrue(t(key), "empty translation for key %s" % key)

    def test_translator_falls_back_to_english(self):
        t = build_translator("xx")
        self.assertEqual(t("menu_exit"), LANGUAGES["en"]["strings"]["menu_exit"])

    def test_detect_system_language_returns_supported(self):
        code = detect_system_language()
        self.assertIn(code, LANGUAGE_ORDER)


if __name__ == "__main__":
    unittest.main()
