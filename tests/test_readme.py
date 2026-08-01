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

Two further guarantees are enforced here:

* The set of dynamic PyPI/GitHub badges stays **exactly** the 5 canonical
  ones (``DYNAMIC_BADGES`` below), each appearing **once** — a duplicated
  badge or a newly invented endpoint (e.g. a 6th ``pypi/dw``) fails.
* The ``Releasing to PyPI`` section keeps documenting the **v* tag flow**
  and stays coherent with ``.github/workflows/release.yml``, which must
  still trigger on ``v*`` tags — so the docs and the release workflow
  cannot silently drift apart.

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
RELEASE_WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "release.yml"

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

# Matches the endpoint of ANY dynamic PyPI / GitHub-tag badge URL present in
# the README (e.g. ``pypi/v/sys-opt``, ``github/v/tag/Leo-Galli/sys-opt``).
# Static ``badge/`` badges (Python 3.8+, Platforms, CLI, ...) are excluded.
# Keep the alternation in sync with the "Reject duplicate or extra dynamic
# badges in README" grep in .github/workflows/ci.yml.
DYNAMIC_BADGE_ENDPOINT_RE = re.compile(
    r"img\.shields\.io/(?:pypi|github/v)/[A-Za-z0-9._/-]+"
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

    def test_no_duplicate_or_extra_dynamic_badges(self):
        # Collect every dynamic PyPI/GitHub badge endpoint that actually
        # appears, count how often each one is used, and compare the
        # multiset against the canonical 5 (each exactly once).
        found = DYNAMIC_BADGE_ENDPOINT_RE.findall(self.readme)
        counts = {}
        for url in found:
            counts[url] = counts.get(url, 0) + 1
        duplicated = [url for url, n in counts.items() if n > 1]
        unknown = sorted(set(found) - set(DYNAMIC_BADGES))
        self.assertEqual(
            (duplicated, unknown), ([], []),
            "README.md must keep exactly the 5 canonical dynamic PyPI/GitHub "
            "badges, each used once. Duplicated: %s. Unknown/extra: %s. "
            "All found: %s" % (duplicated, unknown, sorted(set(found))),
        )

    def test_releasing_section_uses_vstar_tags(self):
        section = re.search(
            r"## .*Releasing to PyPI(.*?)(?=\n## |\Z)", self.readme, re.DOTALL
        )
        self.assertIsNotNone(
            section, "README.md must keep a 'Releasing to PyPI' section"
        )
        text = section.group(1)
        # The section must document the v*-tagged release flow ...
        self.assertIn(
            "v*", text,
            "'Releasing to PyPI' must mention the v* tag pattern",
        )
        self.assertIn(
            "git tag v", text,
            "'Releasing to PyPI' must show a 'git tag vX.Y.Z' example",
        )
        self.assertIn(
            "git push origin v", text,
            "'Releasing to PyPI' must show 'git push origin vX.Y.Z'",
        )
        # ... and stay coherent with the actual release workflow, which must
        # still trigger on v* tags.
        release = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        tags_block = re.search(
            r"tags:\s*\n((?:\s*-\s*[^\n]+\n?)+)", release
        )
        self.assertIsNotNone(tags_block, "release.yml must trigger on tags")
        self.assertIn(
            "v*", tags_block.group(1),
            "release.yml must trigger on v* tags (README coherence)",
        )


if __name__ == "__main__":
    unittest.main()
