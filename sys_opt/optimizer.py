# -*- coding: utf-8 -*-
"""
Multi-OS universal optimizer engine.

Routines adapt to the host OS with zero user configuration. Every step is
wrapped in try/except and reports ok / failed / skipped / skipped-no-elevation
instead of crashing. Elevation is checked before any step runs.
"""

import os
import shutil
import sys

from rich.panel import Panel
from rich.prompt import Prompt

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
        ["reg", "add", r"HKCU\System\GameConfigStore", "/v", "GameDVR_Enabled", "/t", "REG_DWORD", "/d", "0", "/f"],
        ["reg", "add", r"HKCU\System\GameConfigStore", "/v", "GameDVR_FSEBehaviorMode", "/t", "REG_DWORD", "/d", "2", "/f"],
        ["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR", "/v", "AppCaptureEnabled", "/t", "REG_DWORD", "/d", "0", "/f"],
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
# Step assembly + runner
# --------------------------------------------------------------------------- #
def build_steps(t, elevated, dry_run):
    """Return [(localized_label, step_callable)] for the current OS."""
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


def _elevation_instructions(t):
    if os.name == "nt":
        return t("elevation_win")
    return t("elevation_posix")


def run(console, t, dry_run=False, force=False):
    """Run the optimizer: elevation gate, disclaimer, steps, summary."""
    elevated = is_admin()

    if not elevated and not dry_run:
        console.print()
        console.print(
            Panel(
                "[bold yellow]%s[/]\n\n%s" % (t("elevation_title"), _elevation_instructions(t)),
                border_style="yellow",
            )
        )
        proceed = False
        if force:
            proceed = True
        else:
            try:
                answer = Prompt.ask(
                    t("elevation_prompt"), choices=["y", "n"], default="n", show_default=False
                )
                proceed = answer.lower() == "y"
            except Exception:
                proceed = False
        if not proceed:
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
    console.print()
    console.print(
        Panel(
            "[bold green]%s[/] (%s)" % (t("optimize_header"), "dry-run" if dry_run else t("running")),
            border_style="green",
        )
    )

    results = []
    gpu_sched_ok = False
    for label, step in build_steps(t, elevated, dry_run):
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
