# -*- coding: utf-8 -*-
"""
Shared utilities: safe subprocess calls, elevation checks, locale detection
and human-readable formatting. Everything here is written to never raise.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

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


# --------------------------------------------------------------------------- #
# Interactive arrow-key menu (cross-platform) + persistent user config
# --------------------------------------------------------------------------- #


def read_key():
    """Read a single keypress in raw mode; returns a token string.

    Tokens: 'up' / 'down' / 'left' / 'right' / 'enter' / 'exit', a digit
    '1'-'9', or None for any other key. Never raises.
    """
    if os.name == "nt":
        return _read_key_windows()
    return _read_key_unix()


def _read_key_windows():
    try:
        import msvcrt

        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):  # extended key prefix (arrows, ...)
            second = msvcrt.getwch()
            return {"H": "up", "P": "down", "K": "left", "M": "right"}.get(second)
        if ch in ("\r", "\n"):
            return "enter"
        if ch in ("\x1b", "q", "Q", "\x03"):
            return "exit"
        if ch.isdigit() and ch != "0":
            return ch
        return None
    except Exception:
        return None


def _read_key_unix():
    fd = None
    old = None
    try:
        import select
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            readable, _, _ = select.select([sys.stdin], [], [], 0.1)
            if readable:
                rest = sys.stdin.read(2)
                return {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}.get(rest, "exit")
            return "exit"
        if ch in ("\r", "\n"):
            return "enter"
        if ch in ("q", "Q", "\x03"):
            return "exit"
        if ch.isdigit() and ch != "0":
            return ch
        return None
    except Exception:
        return None
    finally:
        if fd is not None and old is not None:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            except Exception:
                pass


def _terminal_width(fallback=88):
    """Best-effort terminal width; used to truncate menu lines so they never
    wrap (wrapping would break the cursor-up re-render math).

    The floor is deliberately low (20): the point of the value is to fit the
    *real* terminal, so on a narrow terminal lines are truncated to its width
    instead of being forced wide and wrapping anyway.
    """
    try:
        import shutil

        size = shutil.get_terminal_size((fallback, 24))
        return max(20, size.columns - 2)
    except Exception:
        return fallback


def _menu_frame(title, items, selected, hint, width=None):
    """Render the selectable menu as plain single-line text (no wrapping)."""
    width = width or _terminal_width()
    lines = [str(title), ""]
    for index, item in enumerate(items):
        marker = "▶" if index == selected else " "
        lines.append(("%s %d. %s" % (marker, index + 1, item))[:width])
    if hint:
        lines.extend(["", hint[:width]])
    return lines


def _enable_vt_windows():
    """Enable ANSI escape processing on Windows consoles (best-effort).

    Without ENABLE_VIRTUAL_TERMINAL_PROCESSING the cursor-up/clear codes used
    by the arrow menu are swallowed by legacy conhost, so frames would stack
    instead of being redrawn in place. Modern terminals already enable VT;
    this is a no-op for them.
    """
    if os.name != "nt":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    except Exception:
        pass


def arrow_menu(console, title, items, hint=None):
    """Interactive arrow-key menu; returns the selected index or None.

    Arrow keys move, Enter selects, Esc / q / 0 cancel, digits 1-9 jump
    straight to an item. When stdin is not a TTY (pipes, CI) or on any
    error it falls back to a numbered rich prompt, so it never blocks a
    script and never crashes.
    """
    if not items:
        return None
    if not sys.stdin.isatty():
        return _numeric_menu(console, title, items)
    try:
        _enable_vt_windows()
        selected = 0
        frame = _menu_frame(title, items, selected, hint)
        for line in frame:
            sys.stdout.write(line + "\n")
        sys.stdout.flush()
        height = len(frame)
        while True:
            key = read_key()
            if key == "up":
                selected = (selected - 1) % len(items)
            elif key == "down":
                selected = (selected + 1) % len(items)
            elif key == "enter":
                return selected
            elif key == "exit":
                return None
            elif key is not None and key.isdigit():
                number = int(key)
                if 1 <= number <= len(items):
                    return number - 1
            else:
                continue  # unknown key: frame stays as-is
            sys.stdout.write("\x1b[%dA\x1b[J" % height)
            frame = _menu_frame(title, items, selected, hint)
            for line in frame:
                sys.stdout.write(line + "\n")
            sys.stdout.flush()
    except Exception:
        return _numeric_menu(console, title, items)


def _numeric_menu(console, title, items):
    """Fallback: numbered rich prompt (used when stdin is not a TTY)."""
    from rich.prompt import Prompt

    console.print()
    console.print(title)
    for index, item in enumerate(items, start=1):
        console.print("  [bold cyan]%d[/]  %s" % (index, item))
    try:
        answer = Prompt.ask(
            "%s [1-%d]" % (title, len(items)),
            choices=[str(i) for i in range(1, len(items) + 1)],
            default="1",
            show_default=False,
        )
        return int(answer) - 1
    except Exception:
        return None


def config_dir(base=None):
    """Directory holding the persistent user config (override for tests)."""
    if base is not None:
        return Path(base)
    return Path.home() / ".sys-opt"


def config_path(base=None):
    """Full path of the persistent user config file."""
    return config_dir(base) / "config.json"


def load_config(base=None):
    """Load the persisted user config; {} on any failure."""
    try:
        data = json.loads(config_path(base).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_config(language, base=None):
    """Persist a user setting (e.g. the chosen language). Never raises."""
    try:
        directory = config_dir(base)
        directory.mkdir(parents=True, exist_ok=True)
        data = load_config(base)
        data["language"] = language
        config_path(base).write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return True
    except Exception:
        return False
