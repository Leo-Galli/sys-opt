# -*- coding: utf-8 -*-
"""
Self-update support: check PyPI for a newer sys-opt release and offer to
install it. Everything here is written to never raise (zero-crash policy):

- ``latest_pypi_version()`` — queries the PyPI JSON API with a short timeout;
  returns ``None`` on any network/parse failure.
- ``needs_update()`` — compares two version strings numerically.
- ``maybe_prompt()`` — called once per day at interactive startup; shows a
  small arrow-key menu when a newer release exists and runs the upgrade if
  the user confirms (the chosen version is remembered, so a decline is not
  nagged about again).
- ``run_update_cli()`` — the ``--update`` flag: check + install, no prompt.
"""

import json
import re
import sys
import time
import urllib.request

from . import __version__
from .utils import arrow_menu, config_dir, config_path, run_cmd

#: PyPI JSON API for the sys-opt package.
_PYPI_JSON_URL = "https://pypi.org/pypi/sys-opt/json"

#: Re-check at most once every 24 hours, so startup stays fast.
_DAILY_SECONDS = 24 * 3600

#: Seconds before a version check gives up (network problems are silent).
_CHECK_TIMEOUT = 4


def version_key(version):
    """Turn a version string into a comparable tuple; never raises.

    ``"1.2.3"`` -> ``(1, 2, 3)``, ``"1.10rc2"`` -> ``(1, 10)`` (pre-release
    suffixes are dropped so ``1.10rc2 < 1.10.0`` compares correctly); garbage
    yields ``(0,)`` so comparisons stay safe.
    """
    try:
        parts = []
        for chunk in str(version or "").split("."):
            match = re.match(r"(\d+)", chunk)
            parts.append(int(match.group(1)) if match else 0)
        return tuple((parts[:3] + [0, 0, 0])[:3])
    except Exception:
        return (0, 0, 0)


def needs_update(latest, current=None):
    """True when ``latest`` is a strictly newer release than ``current``."""
    try:
        return version_key(latest) > version_key(current if current is not None else __version__)
    except Exception:
        return False


def latest_pypi_version(timeout=_CHECK_TIMEOUT):
    """Return the newest published version from PyPI, or None on any failure."""
    try:
        with urllib.request.urlopen(_PYPI_JSON_URL, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
        version = data.get("info", {}).get("version")
        if isinstance(version, str) and version.strip():
            return version.strip()
        return None
    except Exception:
        return None


def _read_config(base=None):
    """Load the user config dict; {} on any failure."""
    try:
        data = json.loads(config_path(base).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _write_config(cfg, base=None):
    """Persist the user config dict; never raises."""
    try:
        directory = config_dir(base)
        directory.mkdir(parents=True, exist_ok=True)
        config_path(base).write_text(
            json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return True
    except Exception:
        return False


def install_update(console, t, latest, timeout=240):
    """Run ``pip install --upgrade sys-opt`` and report the outcome.

    Returns 0 on success, 1 on failure. The manual install command is
    printed on failure (e.g. pip needs elevation or a different environment).
    """
    console.print()
    console.print("[bold cyan]%s[/]" % t("update_installing"))
    rc, _out, _err = run_cmd(
        [sys.executable, "-m", "pip", "install", "--upgrade", "sys-opt"],
        timeout=timeout,
    )
    console.print()
    if rc == 0:
        console.print("[bold green]%s[/]" % (t("update_success") % latest))
        return 0
    console.print("[bold red]%s[/]" % t("update_failed"))
    console.print("[yellow]%s[/]" % t("update_manual"))
    return 1


def maybe_prompt(console, t, base=None):
    """Startup check (once per day): offer to install a newer release.

    Silent in every failure path — offline, same version, already declined.
    When the user confirms, ``pip install --upgrade sys-opt`` runs in-process.
    """
    cfg = _read_config(base)
    try:
        last = float(cfg.get("last_update_check") or 0)
    except (TypeError, ValueError):
        last = 0
    if time.time() - last < _DAILY_SECONDS:
        return
    latest = latest_pypi_version()
    if latest is None:
        return  # offline: stay silent, retry on the next launch
    cfg["last_update_check"] = int(time.time())
    _write_config(cfg, base)
    if not needs_update(latest):
        return
    if cfg.get("update_skipped") == latest:
        return

    from rich.panel import Panel

    console.print()
    console.print(
        Panel(
            "%s\n%s"
            % (
                t("update_available") % latest,
                t("update_current_version") % __version__,
            ),
            title=t("update_title"),
            border_style="cyan",
        )
    )
    index = arrow_menu(
        console, t("update_install_prompt"),
        [t("update_install_now"), t("update_skip")],
        hint=t("menu_arrow_hint"),
    )
    if index == 0:
        install_update(console, t, latest)
        return
    cfg["update_skipped"] = latest
    _write_config(cfg, base)


def run_update_cli(console, t, base=None):
    """The ``--update`` flag: check PyPI and install the newest release.

    Never prompts (works on non-TTY terminals / CI). Returns an exit code:
    0 = up to date or updated, 1 = unreachable or install failed.
    """
    console.print()
    latest = latest_pypi_version()
    if latest is None:
        console.print("[yellow]%s[/]" % t("update_unreachable"))
        return 1
    # Record the check so the interactive daily cache and --update stay
    # consistent (a redundant second check the same day is pointless).
    cfg = _read_config(base)
    cfg["last_update_check"] = int(time.time())
    _write_config(cfg, base)
    if not needs_update(latest):
        console.print("[green]%s[/]" % (t("update_up_to_date") % __version__))
        return 0
    console.print("[cyan]%s[/]" % (t("update_available") % latest))
    return install_update(console, t, latest)
