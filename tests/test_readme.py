# -*- coding: utf-8 -*-
"""
README badge guards — the dynamic badges must never regress to static.

The header of README.md uses shields.io *dynamic* badges so the shown
version, supported Python versions and download counts always come from
the live GitHub tag / PyPI metadata. These tests fail the CI the moment
anyone hardcodes a version literal back into the README (e.g. the old
``img.shields.io/badge/version-1.0.0-...`` badge), and also assert that
the dynamic badges are actually present, so removing them entirely does
not pass vacuously.

Note: the ASCII mock-up of the update prompt legitimately contains
``You have version 1.0.0`` — a *space* form. The guarded pattern uses the
dash form (``version-X.Y.Z``), which only ever appears in static badge
URLs, so that illustration is not a false positive.
"""

import re
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
README = PROJECT_ROOT / "README.md"

# A hardcoded version literal in badge form: "version-1.0.0", "version-2.3.4".
# The dash form is unique to static badge URLs; prose uses "version 1.0.0".
# Case-insensitive so "Version-1.0.0" cannot slip through. Keep in sync with
# the "Reject hardcoded version badges in README" grep in .github/workflows/ci.yml.
HARDCODED_VERSION_RE = re.compile(r"version-\d+(?:\.\d+)+", re.IGNORECASE)

# The dynamic shields.io endpoints the header must keep using.
DYNAMIC_BADGES = (
    "img.shields.io/github/v/tag/Leo-Galli/sys-opt",  # version (GitHub tag)
    "img.shields.io/pypi/v/sys-opt",                  # version (PyPI)
    "img.shields.io/pypi/pyversions/sys-opt",         # supported Python versions
    "img.shields.io/pypi/dm/sys-opt",                 # downloads / month
    "img.shields.io/pypi/dt/sys-opt",                 # total downloads
)


class TestReadmeBadges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README.read_text(encoding="utf-8")

    def test_no_hardcoded_version_in_readme(self):
        matches = HARDCODED_VERSION_RE.findall(self.readme)
        self.assertEqual(
            matches, [],
            "Hardcoded version literal(s) found in README.md: %s. Badges "
            "must stay dynamic (github/v/tag, pypi/v, pypi/pyversions, "
            "pypi/dm, pypi/dt) — never pin a version by hand." % matches,
        )

    def test_dynamic_version_badges_are_present(self):
        missing = [url for url in DYNAMIC_BADGES if url not in self.readme]
        self.assertEqual(
            missing, [],
            "Dynamic badge(s) missing from README.md header: %s" % missing,
        )


if __name__ == "__main__":
    unittest.main()
