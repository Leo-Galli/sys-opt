# -*- coding: utf-8 -*-
"""
Shared utilities: safe subprocess calls, elevation checks, locale detection
and human-readable formatting. Everything here is written to never raise.
"""

import os
import re
import subprocess
import sys
import time

try:
    import psutil
except Exception:  # pragma: no cover - optional dependency
    psutil = None

NA = "N/A"


def run_cmd(args, timeout=30, shell=False, env=None):
    """Run a subprocess safely; never raises.

    Returns ``(returncode, stdout, stderr)`` with stripped strings.
    """
    try:
        proc = subprocess.run(
            args,
            shell=shell,
            timeout=timeout,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()
        return proc.returncode, stdout, stderr
    except FileNotFoundError:
        return -1, "", "command not found"
    except subprocess.TimeoutExpired:
        return -1, "", "timed out"
    except Exception as exc:  # zero-crash policy
        return -1, "", str(exc)


def is_admin():
    """Return True when running elevated (Administrator / root / sudo)."""
    try:
        if os.name == "nt":
            import ctypes

            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        return os.geteuid() == 0
    except Exception:
        return False


def format_bytes(value):
    """Format a byte count as a human-readable string; never raises."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return NA
    if value < 0:
        return NA
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return "%d B" % int(value)
            return "%.2f %s" % (value, unit)
        value /= 1024.0
    return NA


def format_freq(hz):
    """Format a frequency in Hertz as GHz/MHz/kHz; never raises."""
    try:
        hz = float(hz)
    except (TypeError, ValueError):
        return NA
    if hz <= 0:
        return NA
    if hz >= 1e9:
        return "%.2f GHz" % (hz / 1e9)
    if hz >= 1e6:
        return "%.0f MHz" % (hz / 1e6)
    return "%.0f kHz" % (hz / 1e3)


def format_uptime(seconds):
    """Format seconds as '3d 4h 12m 5s'; 'N/A' when unknown."""
    try:
        seconds = int(float(seconds))
    except (TypeError, ValueError):
        return NA
    if seconds < 0:
        return NA
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if days:
        parts.append("%dd" % days)
    if hours or days:
        parts.append("%dh" % hours)
    if minutes or hours or days:
        parts.append("%dm" % minutes)
    parts.append("%ds" % secs)
    return " ".join(parts)


def get_uptime():
    """Return system uptime in seconds, or None if unavailable."""
    if psutil is not None:
        try:
            return max(0.0, time.time() - psutil.boot_time())
        except Exception:
            pass
    if os.name == "nt":
        try:
            import ctypes

            return ctypes.windll.kernel32.GetTickCount64() / 1000.0
        except Exception:
            return None
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/uptime", "r", encoding="utf-8", errors="replace") as handle:
                return float(handle.read().split()[0])
        except Exception:
            return None
    if sys.platform == "darwin":
        _rc, out, _err = run_cmd(["sysctl", "-n", "kern.boottime"])
        match = re.search(r"sec\s*=\s*(\d+)", out)
        if match:
            try:
                return max(0.0, time.time() - int(match.group(1)))
            except Exception:
                return None
    return None
