# -*- coding: utf-8 -*-
"""
Multi-OS universal optimizer engine.

Routines adapt to the host OS with zero user configuration. Every step is
wrapped in try/except and reports ok / failed / skipped / skipped-no-elevation
instead of crashing. Elevation is checked before any step runs.
"""

import os
import re
import shutil
import sys

from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from .utils import is_admin, run_cmd

HIGH_PERFORMANCE_GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
ULTIMATE_PERFORMANCE_GUID = "e9a42b02-d5df-448d-aa00-03f14749eb61"

_STATUS_KEYS = {
    "ok": "status_ok",
    "failed": "status_failed",
    "skipped": "status_skipped",
    "skipped_no_elev": "status_skipped_no_elev",
}

_STATUS_COLORS = {
    "ok": "green",
    "failed": "red",
    "skipped": "yellow",
    "skipped_no_elev": "yellow",
}


def _purge_directory(path):
    """Best-effort recursive file removal; returns number of files removed."""
    removed = 0
    if not os.path.isdir(path):
        return removed
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            try:
                os.remove(os.path.join(root, name))
                removed += 1
            except Exception:
                pass
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except Exception:
                pass
    return removed


def _count_files(path, cap=500):
    """Count files under ``path`` with a hard cap; never raises."""
    if not os.path.isdir(path):
        return 0
    total = 0
    try:
        for _root, _dirs, files in os.walk(path):
            total += len(files)
            if total >= cap:
                return cap
    except Exception:
        return 0
    return total


# --------------------------------------------------------------------------- #
# Windows steps
# --------------------------------------------------------------------------- #
def _step_win_temp(t, elevated, dry_run):
    user_temp = os.environ.get("TEMP") or os.path.join(
        os.environ.get("USERPROFILE", ""), "AppData", "Local", "Temp"
    )
    system_temp = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Temp")
    targets = [path for path in (user_temp, system_temp) if os.path.isdir(path)]
    if dry_run:
        return "ok", "; ".join(targets) or t("na")
    if not targets:
        return "skipped", t("na")
    count = 0
    for target in targets:
        count += _purge_directory(target)
    return "ok", "%d" % count


def _step_win_services(t, elevated, dry_run):
    services = ("SysMain", "Superfetch")
    if dry_run:
        return "ok", ", ".join(services)
    outcomes = []
    for service in services:
        _rc_stop, _out, err_stop = run_cmd(["sc", "stop", service], timeout=25)
        _rc_cfg, _out2, err_cfg = run_cmd(["sc", "config", service, "start=", "disabled"], timeout=25)
        combined = "%s %s" % (err_stop, err_cfg)
        lowered = combined.lower()
        service_missing = ("1060" in combined) or ("specified service" in lowered and "does not exist" in lowered)
        already_inactive = ("1062" in combined) or ("1058" in combined)
        if service_missing:
            outcomes.append("skipped")
        elif already_inactive or _rc_stop == 0 or _rc_cfg == 0:
            outcomes.append("ok")
        else:
            outcomes.append("failed")
    if "ok" in outcomes:
        return "ok", ", ".join(services)
    if all(status == "skipped" for status in outcomes):
        return "skipped", t("na")
    return "failed", ", ".join(services)


def _step_win_power(t, elevated, dry_run):
    if dry_run:
        return "ok", "High Performance"
    rc, _out, _err = run_cmd(["powercfg", "-setactive", HIGH_PERFORMANCE_GUID], timeout=20)
    if rc == 0:
        return "ok", "High Performance"
    rc2, _out2, _err2 = run_cmd(
        ["powercfg", "-duplicatescheme", ULTIMATE_PERFORMANCE_GUID], timeout=20
    )
    if rc2 == 0:
        run_cmd(["powercfg", "-setactive", ULTIMATE_PERFORMANCE_GUID], timeout=20)
        return "ok", "Ultimate Performance"
    return "failed", t("na")


def _step_win_dns(t, elevated, dry_run):
    if dry_run:
        return "ok", "ipconfig /flushdns"
    rc, _out, _err = run_cmd(["ipconfig", "/flushdns"], timeout=20)
    return ("ok" if rc == 0 else "failed"), t("na")


def _step_win_gpu_sched(t, elevated, dry_run):
    """Enable hardware-accelerated GPU scheduling (HAGS) - less CPU overhead in games."""
    command = [
        "reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
        "/v", "HwSchMode", "/t", "REG_DWORD", "/d", "2", "/f",
    ]
    if dry_run:
        return "ok", " ".join(command)
    if not elevated:
        return "skipped_no_elev", t("na")
    rc, _out, _err = run_cmd(command, timeout=20)
    return ("ok" if rc == 0 else "failed"), t("na")


def _step_win_game_dvr(t, elevated, dry_run):
    """Disable Game DVR / Game Bar background recording (removes capture overhead)."""
    commands = [
        [
            "reg", "add", r"HKCU\System\GameConfigStore",
            "/v", "GameDVR_Enabled", "/t", "REG_DWORD", "/d", "0", "/f",
        ],
        [
            "reg", "add", r"HKCU\System\GameConfigStore",
            "/v", "GameDVR_FSEBehaviorMode", "/t", "REG_DWORD", "/d", "2", "/f",
        ],
        [
            "reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR",
            "/v", "AppCaptureEnabled", "/t", "REG_DWORD", "/d", "0", "/f",
        ],
    ]
    if dry_run:
        return "ok", "; ".join(" ".join(c) for c in commands)
    success = 0
    for command in commands:
        rc, _out, _err = run_cmd(command, timeout=20)
        if rc == 0:
            success += 1
    return ("ok" if success == len(commands) else "failed"), "%d/%d" % (success, len(commands))


def _step_win_update_cache(t, elevated, dry_run):
    cache_dir = os.path.join(
        os.environ.get("SystemRoot", r"C:\Windows"), "SoftwareDistribution", "Download"
    )
    if dry_run:
        return "ok", cache_dir
    if not os.path.isdir(cache_dir):
        return "skipped", t("na")
    if not elevated:
        return "skipped_no_elev", cache_dir
    count = _purge_directory(cache_dir)
    return "ok", "%d" % count


# --------------------------------------------------------------------------- #
# macOS steps
# --------------------------------------------------------------------------- #
def _step_mac_caches(t, elevated, dry_run):
    if dry_run:
        return "ok", "~/Library/Caches, /Library/Caches"
    home = os.path.expanduser("~")
    targets = []
    if home:
        targets.append(os.path.join(home, "Library", "Caches"))
    targets.append("/Library/Caches")
    count = 0
    touched = False
    for target in targets:
        if not os.path.isdir(target):
            continue
        touched = True
        if elevated or not target.startswith("/Library/Caches"):
            count += _purge_directory(target)
    return ("ok", "%d" % count) if touched else ("skipped", t("na"))


def _step_mac_dns(t, elevated, dry_run):
    if dry_run:
        return "ok", "dscacheutil -flushcache; killall -HUP mDNSResponder"
    rc1, _out, _err1 = run_cmd(["dscacheutil", "-flushcache"], timeout=20)
    rc2, _out, _err2 = run_cmd(["killall", "-HUP", "mDNSResponder"], timeout=20)
    return ("ok" if rc1 == 0 or rc2 == 0 else "failed"), t("na")


def _step_mac_purge(t, elevated, dry_run):
    if dry_run:
        return "ok", "purge"
    if not elevated:
        return "skipped_no_elev", t("na")
    rc, _out, _err = run_cmd(["purge"], timeout=90)
    return ("ok" if rc == 0 else "failed"), t("na")


# --------------------------------------------------------------------------- #
# Linux steps
# --------------------------------------------------------------------------- #
def _step_linux_tmp(t, elevated, dry_run):
    if dry_run:
        return "ok", "/tmp"
    if not os.path.isdir("/tmp"):
        return "skipped", t("na")
    count = _purge_directory("/tmp")
    return "ok", "%d" % count


def _step_linux_drop_caches(t, elevated, dry_run):
    if dry_run:
        return "ok", "echo 3 > /proc/sys/vm/drop_caches"
    if not elevated:
        return "skipped_no_elev", t("na")
    try:
        with open("/proc/sys/vm/drop_caches", "w", encoding="utf-8") as handle:
            handle.write("3\n")
        return "ok", t("na")
    except Exception:
        return "failed", t("na")


_PKG_CLEAN_COMMANDS = {
    "apt": ["apt", "clean"],
    "dnf": ["dnf", "clean", "all"],
    "pacman": ["pacman", "-Sc", "--noconfirm"],
    "zypper": ["zypper", "clean"],
    "apk": ["apk", "cache", "clean"],
}


def _detect_pkg_manager():
    for manager in _PKG_CLEAN_COMMANDS:
        if shutil.which(manager):
            return manager
    return None


def _step_linux_pkg_cache(t, elevated, dry_run):
    manager = _detect_pkg_manager()
    if not manager:
        return "skipped", t("na")
    command = _PKG_CLEAN_COMMANDS[manager]
    if dry_run:
        return "ok", " ".join(command)
    rc, _out, _err = run_cmd(command, timeout=180)
    return ("ok" if rc == 0 else "failed"), t("na")


# --------------------------------------------------------------------------- #
# Read-only state detection for --optimize --suggest
# --------------------------------------------------------------------------- #
#: Each detector returns ``(status, detail)`` where status is one of:
#:   ready            - the step would improve this system (worth applying)
#:   applied          - already in the desired state (nothing to do)
#:   needs_elevation  - only useful when running elevated
#:   not_applicable   - not relevant on this machine (missing service / dir / pkg)
#: Detection NEVER modifies anything: it only inspects.


def _detect_win_temp(elevated):
    user_temp = os.environ.get("TEMP") or os.path.join(
        os.environ.get("USERPROFILE", ""), "AppData", "Local", "Temp"
    )
    system_temp = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Temp")
    targets = [path for path in (user_temp, system_temp) if os.path.isdir(path)]
    if not targets:
        return "not_applicable", ""
    total = sum(_count_files(path) for path in targets)
    if total == 0:
        return "applied", "0 files"
    return "ready", "%d files" % total


def _detect_win_services(elevated):
    results = []
    for service in ("SysMain", "Superfetch"):
        rc, out, _err = run_cmd(["sc", "qc", service], timeout=20)
        if rc == 0:
            results.append("applied" if "DISABLED" in out.upper() else "ready")
    if not results:
        return "not_applicable", ""
    if all(status == "applied" for status in results):
        return "applied", "SysMain, Superfetch"
    return "ready", "SysMain, Superfetch"


def _detect_win_power(elevated):
    rc, out, _err = run_cmd(["powercfg", "/getactivescheme"], timeout=20)
    if rc == 0 and (HIGH_PERFORMANCE_GUID in out or ULTIMATE_PERFORMANCE_GUID in out):
        return "applied", "High Performance"
    return "ready", "powercfg -setactive"


def _detect_win_dns(elevated):
    return "ready", "ipconfig /flushdns"


def _detect_win_gpu_sched(elevated):
    _rc, out, _err = run_cmd(
        ["reg", "query", r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "/v", "HwSchMode"],
        timeout=20,
    )
    if _rc == 0 and "0x2" in out:
        return "applied", "HAGS on"
    return "ready", "HwSchMode=2"


def _detect_win_game_dvr(elevated):
    _rc, out, _err = run_cmd(
        ["reg", "query", r"HKCU\System\GameConfigStore", "/v", "GameDVR_Enabled"],
        timeout=20,
    )
    if _rc == 0 and "0x0" in out:
        return "applied", "Game DVR off"
    return "ready", "GameDVR_Enabled=0"


def _detect_win_update_cache(elevated):
    cache_dir = os.path.join(
        os.environ.get("SystemRoot", r"C:\Windows"), "SoftwareDistribution", "Download"
    )
    if not os.path.isdir(cache_dir):
        return "not_applicable", ""
    count = _count_files(cache_dir)
    return ("applied", "0 files") if count == 0 else ("ready", "%d files" % count)


def _detect_mac_caches(elevated):
    home = os.path.expanduser("~")
    targets = []
    if home:
        targets.append(os.path.join(home, "Library", "Caches"))
    targets.append("/Library/Caches")
    total = sum(_count_files(path) for path in targets)
    if total == 0:
        return "applied", "0 files"
    return "ready", "%d files" % total


def _detect_mac_dns(elevated):
    return "ready", "dscacheutil -flushcache"


def _detect_mac_purge(elevated):
    if not elevated:
        return "needs_elevation", "sudo purge"
    return "ready", "purge"


def _detect_linux_tmp(elevated):
    if not os.path.isdir("/tmp"):
        return "not_applicable", ""
    count = _count_files("/tmp")
    return ("applied", "0 files") if count == 0 else ("ready", "%d files" % count)


def _detect_linux_drop_caches(elevated):
    if not elevated:
        return "needs_elevation", "root required"
    return "ready", "vm.drop_caches=3"


def _detect_linux_pkg_cache(elevated):
    manager = _detect_pkg_manager()
    if not manager:
        return "not_applicable", ""
    return "ready", manager


#: step -> detector callable (all take an ``elevated`` bool).
_DETECT_STEPS = {
    _step_win_temp: _detect_win_temp,
    _step_win_services: _detect_win_services,
    _step_win_power: _detect_win_power,
    _step_win_dns: _detect_win_dns,
    _step_win_gpu_sched: _detect_win_gpu_sched,
    _step_win_game_dvr: _detect_win_game_dvr,
    _step_win_update_cache: _detect_win_update_cache,
    _step_mac_caches: _detect_mac_caches,
    _step_mac_dns: _detect_mac_dns,
    _step_mac_purge: _detect_mac_purge,
    _step_linux_tmp: _detect_linux_tmp,
    _step_linux_drop_caches: _detect_linux_drop_caches,
    _step_linux_pkg_cache: _detect_linux_pkg_cache,
}


#: step -> estimated impact per profile (1-5 stars); missing profiles fall back to "all".
_STEP_IMPACT = {
    _step_win_gpu_sched: {"all": 4, "gaming": 5, "ai": 2, "studio": 1, "clean": 1},
    _step_win_game_dvr: {"all": 4, "gaming": 5, "ai": 1, "studio": 1, "clean": 1},
    _step_win_power: {"all": 3, "gaming": 5, "ai": 3, "studio": 2, "clean": 1},
    _step_win_services: {"all": 3, "gaming": 4, "ai": 3, "studio": 2, "clean": 1},
    _step_win_temp: {"all": 2, "clean": 3, "studio": 2},
    _step_win_dns: {"all": 1},
    _step_win_update_cache: {"all": 1, "clean": 2},
    _step_mac_caches: {"all": 2, "clean": 3, "studio": 2},
    _step_mac_dns: {"all": 1},
    _step_mac_purge: {"all": 2, "gaming": 3, "ai": 3},
    _step_linux_tmp: {"all": 2, "clean": 3, "studio": 2},
    _step_linux_drop_caches: {"all": 3, "ai": 4, "gaming": 3},
    _step_linux_pkg_cache: {"all": 2, "clean": 3},
}


#: step -> i18n key explaining why the step helps.
_STEP_WHY = {
    _step_win_temp: "suggest_why_temp",
    _step_win_services: "suggest_why_service",
    _step_win_power: "suggest_why_power",
    _step_win_dns: "suggest_why_dns",
    _step_win_gpu_sched: "suggest_why_gpu_sched",
    _step_win_game_dvr: "suggest_why_game_dvr",
    _step_win_update_cache: "suggest_why_update_cache",
    _step_mac_caches: "suggest_why_cache",
    _step_mac_dns: "suggest_why_dns",
    _step_mac_purge: "suggest_why_purge",
    _step_linux_tmp: "suggest_why_tmp",
    _step_linux_drop_caches: "suggest_why_drop_caches",
    _step_linux_pkg_cache: "suggest_why_pkg_cache",
}


#: detect status -> i18n key and color for the suggestion table.
_SUGGEST_STATUS_KEYS = {
    "ready": "suggest_status_ready",
    "applied": "suggest_status_applied",
    "needs_elevation": "suggest_status_needs_elevation",
    "not_applicable": "suggest_status_not_applicable",
}

_SUGGEST_STATUS_COLORS = {
    "ready": "green",
    "applied": "dim",
    "needs_elevation": "yellow",
    "not_applicable": "dim",
}


# --------------------------------------------------------------------------- #
# Step assembly + runner
# --------------------------------------------------------------------------- #
#: Optimization profiles (order used by the interactive chooser).
PROFILE_ORDER = ["all", "gaming", "ai", "studio", "clean"]

#: Profile code -> i18n key for its label.
PROFILE_LABEL_KEYS = {
    "all": "profile_all",
    "gaming": "profile_gaming",
    "ai": "profile_ai",
    "studio": "profile_studio",
    "clean": "profile_clean",
}

#: Which profiles include each step. Steps without an entry run in every profile.
_STEP_PROFILES = {
    _step_win_temp: {"all", "gaming", "ai", "studio", "clean"},
    _step_win_services: {"all", "gaming", "ai", "studio"},
    _step_win_power: {"all", "gaming", "ai"},
    _step_win_gpu_sched: {"all", "gaming"},
    _step_win_game_dvr: {"all", "gaming"},
    _step_win_dns: {"all", "gaming", "ai", "studio", "clean"},
    _step_win_update_cache: {"all", "gaming", "ai", "studio", "clean"},
    _step_mac_caches: {"all", "gaming", "ai", "studio", "clean"},
    _step_mac_dns: {"all", "gaming", "ai", "studio", "clean"},
    _step_mac_purge: {"all", "gaming", "ai"},
    _step_linux_tmp: {"all", "gaming", "ai", "studio", "clean"},
    _step_linux_drop_caches: {"all", "gaming", "ai"},
    _step_linux_pkg_cache: {"all", "gaming", "ai", "studio", "clean"},
}


def _steps_for_os(t):
    """Return every step for the current OS, in execution order."""
    if os.name == "nt":
        return [
            (t("step_temp"), _step_win_temp),
            (t("step_service"), _step_win_services),
            (t("step_power"), _step_win_power),
            (t("step_gpu_sched"), _step_win_gpu_sched),
            (t("step_game_dvr"), _step_win_game_dvr),
            (t("step_dns"), _step_win_dns),
            (t("step_update_cache"), _step_win_update_cache),
        ]
    if sys.platform == "darwin":
        return [
            (t("step_cache"), _step_mac_caches),
            (t("step_dns"), _step_mac_dns),
            (t("step_purge"), _step_mac_purge),
        ]
    return [
        (t("step_tmp"), _step_linux_tmp),
        (t("step_drop_caches"), _step_linux_drop_caches),
        (t("step_pkg_cache"), _step_linux_pkg_cache),
    ]


def build_steps(t, elevated, dry_run, profile="all"):
    """Return [(localized_label, step_callable)] for the current OS & profile.

    ``profile`` must be one of PROFILE_ORDER; 'all' returns every step.
    """
    steps = _steps_for_os(t)
    if profile == "all":
        return steps
    return [
        (label, step)
        for (label, step) in steps
        if profile in _STEP_PROFILES.get(step, set(PROFILE_ORDER))
    ]


def _elevation_instructions(t):
    if os.name == "nt":
        return t("elevation_win")
    return t("elevation_posix")


def _elevation_gate(console, t, force):
    """Ask whether to continue without elevation; returns True to proceed."""
    console.print()
    console.print(
        Panel(
            "[bold yellow]%s[/]\n\n%s" % (t("elevation_title"), _elevation_instructions(t)),
            border_style="yellow",
        )
    )
    if force:
        return True
    try:
        answer = Prompt.ask(
            t("elevation_prompt"), choices=["y", "n"], default="n", show_default=False
        )
        return answer.lower() == "y"
    except Exception:
        return False


def run(console, t, dry_run=False, force=False, profile="all"):
    """Run the optimizer: elevation gate, disclaimer, steps, summary."""
    elevated = is_admin()

    if not elevated and not dry_run:
        if not _elevation_gate(console, t, force):
            console.print(t("elevation_abort"))
            return 0
        console.print(t("running_without_elevation"))

    console.print()
    console.print(
        Panel(
            "[bold yellow]%s[/]\n%s" % (t("warning_title"), t("disclaimer")),
            border_style="yellow",
        )
    )
    profile_label = t(PROFILE_LABEL_KEYS.get(profile, PROFILE_LABEL_KEYS["all"]))
    console.print()
    console.print(
        Panel(
            "[bold green]%s[/] · %s (%s)"
            % (t("optimize_header"), profile_label, "dry-run" if dry_run else t("running")),
            border_style="green",
        )
    )

    results = []
    gpu_sched_ok = False
    for label, step in build_steps(t, elevated, dry_run, profile=profile):
        try:
            if not dry_run:
                with console.status("[bold]%s[/] ..." % label):
                    status, detail = step(t, elevated, dry_run)
            else:
                status, detail = step(t, elevated, dry_run)
        except Exception:  # zero-crash policy
            status, detail = "failed", t("na")
        if step is _step_win_gpu_sched and status == "ok":
            gpu_sched_ok = True
        results.append((label, status, detail))

    for label, status, detail in results:
        color = _STATUS_COLORS.get(status, "white")
        status_text = t(_STATUS_KEYS.get(status, "status_failed"))
        line = "  [bold]%s[/]  [%s]%s[/]" % (label, color, status_text)
        console.print(line)
        if detail and detail != t("na"):
            console.print("      [dim]%s[/]" % detail)

    ok_count = sum(1 for _label, status, _detail in results if status == "ok")
    failed_count = sum(1 for _label, status, _detail in results if status == "failed")
    console.print()
    console.print(
        Panel(
            "[bold green]%s[/]  -  [green]%d %s[/]   [red]%d %s[/]"
            % (t("optimize_summary"), ok_count, t("status_ok"), failed_count, t("status_failed")),
            border_style="green",
        )
    )
    if gpu_sched_ok:
        console.print()
        console.print("[bold yellow]⚠ %s[/]" % t("reboot_required"))
    return 0 if failed_count == 0 else 1


def _step_impact(step, profile):
    """Estimated FPS/performance impact of a step for a profile (1-5 stars)."""
    impact = _STEP_IMPACT.get(step, {})
    return impact.get(profile, impact.get("all", 2))


def _parse_apply_selection(answer, rows):
    """Map a user answer to the actionable rows to apply.

    Accepts ``all``, ``none``, or comma/space separated 1-based numbers that
    match the numbering shown in the suggestion table. Rows that are not
    actionable (already applied / not applicable) are never returned.
    """
    answer = (answer or "").strip().lower()
    numbered = {row["_num"]: row for row in rows if row.get("_num")}
    if answer in ("all", "a", "yes", "y"):
        return [numbered[n] for n in sorted(numbered)]
    if answer in ("none", "no", "n", ""):
        return []
    selected = []
    for part in re.split(r"[\s,;]+", answer):
        if part.isdigit() and int(part) in numbered:
            selected.append(numbered[int(part)])
    return selected


def suggest(console, t, profile="all", dry_run=False, force=False):
    """Inspect the system and propose the most impactful optimizations.

    Detection is strictly read-only: nothing is applied until the user
    explicitly confirms (all / none / a subset by number). With --dry-run
    the ranked suggestions are shown and nothing is ever applied.
    """
    elevated = is_admin()
    profile_label = t(PROFILE_LABEL_KEYS.get(profile, PROFILE_LABEL_KEYS["all"]))
    console.print()
    console.print(
        Panel(
            "[bold cyan]%s[/] · %s" % (t("suggest_header"), profile_label),
            border_style="cyan",
        )
    )

    rows = []
    for label, step in build_steps(t, elevated, False, profile=profile):
        detect = _DETECT_STEPS.get(step)
        if detect is None:
            status, detail = "ready", ""
        else:
            try:
                status, detail = detect(elevated)
            except Exception:
                status, detail = "ready", t("na")
        rows.append(
            {
                "label": label,
                "step": step,
                "status": status,
                "detail": detail,
                "impact": _step_impact(step, profile),
                "why": t(_STEP_WHY.get(step, "suggest_why_dns")),
            }
        )

    # Rank: actionable first (by impact desc), then already-applied / not-applicable.
    order = {"ready": 0, "needs_elevation": 1, "applied": 2, "not_applicable": 3}
    rows.sort(key=lambda row: (order.get(row["status"], 4), -row["impact"], row["label"]))

    # Number only actionable rows, so the confirmation maps 1:1 to the table.
    counter = 0
    for row in rows:
        if row["status"] in ("ready", "needs_elevation"):
            counter += 1
            row["_num"] = counter
        else:
            row["_num"] = None

    table = Table(title=t("suggest_header"), title_justify="left")
    table.add_column("#", style="dim")
    table.add_column(t("suggest_col_step"), style="bold")
    table.add_column(t("suggest_col_impact"), justify="center")
    table.add_column(t("suggest_col_status"))
    table.add_column(t("suggest_col_why"))
    for row in rows:
        status_key = _SUGGEST_STATUS_KEYS.get(row["status"], "suggest_status_ready")
        color = _SUGGEST_STATUS_COLORS.get(row["status"], "white")
        stars = "★" * row["impact"]
        table.add_row(
            str(row["_num"]) if row["_num"] else "—",
            row["label"],
            "[yellow]%s[/]" % stars if row["impact"] else "—",
            "[%s]%s[/]" % (color, t(status_key)),
            "[dim]%s[/]" % row["why"],
        )
    console.print(table)
    console.print("[dim]%s[/]" % t("suggest_impact_legend"))

    actionable = [row for row in rows if row["status"] in ("ready", "needs_elevation")]
    if not actionable:
        console.print()
        console.print("[bold green]✓ %s[/]" % t("suggest_nothing"))
        return 0

    if dry_run:
        console.print()
        console.print("[bold yellow]%s[/]" % t("suggest_dry_run_note"))
        return 0

    # Ask for the selection FIRST: a user who types 'none' must never see a
    # pointless elevation prompt. Only confirmed selections hit the gate.
    try:
        answer = Prompt.ask(t("suggest_apply_prompt"), default="none", show_default=False)
    except Exception:
        answer = "none"
    selected = _parse_apply_selection(answer, rows)
    if not selected:
        console.print(t("suggest_abort"))
        return 0

    if not elevated:
        if not _elevation_gate(console, t, force):
            console.print(t("elevation_abort"))
            return 0
        console.print(t("running_without_elevation"))

    console.print()
    console.print("[bold green]%s[/]" % t("suggest_applying"))
    results = []
    for row in selected:
        label, step = row["label"], row["step"]
        try:
            with console.status("[bold]%s[/] ..." % label):
                status, detail = step(t, elevated, False)
        except Exception:  # zero-crash policy
            status, detail = "failed", t("na")
        results.append((label, status, detail))

    for label, status, detail in results:
        color = _STATUS_COLORS.get(status, "white")
        status_text = t(_STATUS_KEYS.get(status, "status_failed"))
        console.print("  [bold]%s[/]  [%s]%s[/]" % (label, color, status_text))
        if detail and detail != t("na"):
            console.print("      [dim]%s[/]" % detail)

    ok_count = sum(1 for _label, status, _detail in results if status == "ok")
    failed_count = sum(1 for _label, status, _detail in results if status == "failed")
    console.print()
    console.print(
        Panel(
            "[bold green]%s[/]  -  [green]%d %s[/]   [red]%d %s[/]"
            % (t("optimize_summary"), ok_count, t("status_ok"), failed_count, t("status_failed")),
            border_style="green",
        )
    )
    return 0 if failed_count == 0 else 1
