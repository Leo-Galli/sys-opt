# -*- coding: utf-8 -*-
"""sys-opt entry point: CLI flags + interactive terminal menu."""

import argparse
import sys

from . import __version__
from .i18n.languages import (
    LANGUAGE_ORDER,
    LANGUAGES,
    build_translator,
    detect_system_language,
)
from . import benchmark, inspector, optimizer


def _ensure_utf8_output():
    """Force UTF-8 with errors='replace' on stdout/stderr so emoji and
    non-ASCII labels never crash the CLI on legacy Windows consoles."""
    for stream in (sys.stdout, sys.stderr):
        try:
            reconfigure = getattr(stream, "reconfigure", None)
            if reconfigure is not None:
                reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_SYS_OPT_BANNER = (
    " ███████╗██╗   ██╗███████╗      ██████╗ ██████╗ ████████╗"
    "\n ██╔════╝╚██╗ ██╔╝██╔════╝     ██╔═══██╗██╔═══██╗╚══██╔══╝"
    "\n ███████╗ ╚████╔╝ ███████╗     ██║   ██║██║   ██║   ██║"
    "\n ╚════██║  ╚██╔╝  ╚════██║     ██║   ██║██║   ██║   ██║"
    "\n ███████║   ██║   ███████║     ╚██████╔╝╚██████╔╝   ██║"
    "\n ╚══════╝   ╚═╝   ╚══════╝      ╚═════╝  ╚═════╝    ╚═╝"
)


def _make_console():
    from rich.console import Console

    return Console()


def _print_languages(console):
    from rich.table import Table

    table = Table(title="Supported Languages", title_justify="left")
    table.add_column("#")
    table.add_column("Code")
    table.add_column("Language", style="bold")
    table.add_column("Native")
    table.add_column("Direction")
    for index, code in enumerate(LANGUAGE_ORDER, start=1):
        meta = LANGUAGES[code]
        table.add_row(
            str(index), code, meta["name"], "%s %s" % (meta["flag"], meta["native"]), meta["dir"]
        )
    console.print(table)


def _choose_language(console, t):
    _print_languages(console)
    detected = detect_system_language()
    default_native = LANGUAGES[detected]["native"]
    from rich.prompt import Prompt

    prompt_text = "%s [1-%d] (%s: %s):" % (
        t("lang_prompt"),
        len(LANGUAGE_ORDER),
        t("lang_auto"),
        default_native,
    )
    try:
        choice = Prompt.ask(prompt_text, default="0", show_default=False)
        choice_int = int(choice)
    except Exception:
        choice_int = 0
    if 1 <= choice_int <= len(LANGUAGE_ORDER):
        return LANGUAGE_ORDER[choice_int - 1]
    return detected


def _main_menu(console, t):
    from rich.panel import Panel
    from rich.table import Table

    table = Table(box=None, show_header=False, padding=(0, 2))
    table.add_column()
    table.add_row("[bold cyan][1][/] 🔍 %s" % t("menu_inspect"))
    table.add_row("[bold cyan][2][/] 🚀 %s" % t("menu_optimize"))
    table.add_row("[bold cyan][3][/] ⚡ %s" % t("menu_suite"))
    table.add_row("[bold cyan][4][/] 📊 %s" % t("menu_benchmark"))
    table.add_row("[bold cyan][5][/] 🌐 %s" % t("menu_language"))
    table.add_row("[bold cyan][0][/] 🚪 %s" % t("menu_exit"))
    console.print(
        Panel(
            table,
            title="[bold]%s[/]" % t("app_title"),
            subtitle=t("tagline"),
            border_style="cyan",
        )
    )


def _print_banner(console):
    """Print the ASCII-art brand banner (language-independent)."""
    from rich.panel import Panel
    from rich.text import Text

    console.print(Panel(Text(_SYS_OPT_BANNER, style="bold cyan"), border_style="cyan"))


def _choose_profile(console, t):
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table

    table = Table(box=None, show_header=False, padding=(0, 2))
    table.add_column()
    for index, code in enumerate(optimizer.PROFILE_ORDER, start=1):
        table.add_row(
            "[bold cyan][%d][/] %s" % (index, t(optimizer.PROFILE_LABEL_KEYS[code]))
        )
    console.print(Panel(table, title="[bold]%s[/]" % t("profile_prompt"), border_style="cyan"))
    try:
        choice = Prompt.ask(t("profile_prompt"), default="1", show_default=False)
        choice_int = int(choice)
    except Exception:
        choice_int = 1
    if 1 <= choice_int <= len(optimizer.PROFILE_ORDER):
        return optimizer.PROFILE_ORDER[choice_int - 1]
    return "all"


def _pause(console, t):
    try:
        console.input(t("press_enter"))
    except Exception:
        pass


def _interactive(console, initial_language):
    from rich.prompt import Prompt

    language = initial_language
    t = build_translator(language)
    console.print()
    _print_banner(console)
    while True:
        console.print()
        _main_menu(console, t)
        try:
            choice = Prompt.ask(
                t("menu_prompt"), choices=["0", "1", "2", "3", "4", "5"], default="0", show_default=False
            )
        except Exception:
            choice = "0"
        if choice == "1":
            inspector.run(console, t, rtl=LANGUAGES[language]["dir"] == "rtl")
            _pause(console, t)
        elif choice == "2":
            optimizer.run(console, t, profile=_choose_profile(console, t))
            _pause(console, t)
        elif choice == "3":
            profile = _choose_profile(console, t)
            inspector.run(console, t, rtl=LANGUAGES[language]["dir"] == "rtl")
            optimizer.run(console, t, profile=profile)
            _pause(console, t)
        elif choice == "4":
            benchmark.run(console, t)
            _pause(console, t)
        elif choice == "5":
            language = _choose_language(console, t)
            t = build_translator(language)
            console.print(
                "[bold green]✓ %s: %s %s[/]"
                % (t("lang_selected"), LANGUAGES[language]["flag"], LANGUAGES[language]["native"])
            )
            _pause(console, t)
        else:
            console.print()
            console.print("[bold green]%s[/]" % t("goodbye"))
            return 0


def main(argv=None):
    _ensure_utf8_output()
    parser = argparse.ArgumentParser(
        prog="sys-opt",
        description="Universal Hardware Inspector & Multi-OS Optimizer (10+ languages).",
    )
    parser.add_argument("--inspect", action="store_true", help="Inspect hardware specs and exit.")
    parser.add_argument("--optimize", action="store_true", help="Run system optimization and exit.")
    parser.add_argument("--suite", action="store_true", help="Inspect then optimize, then exit.")
    parser.add_argument("--benchmark", action="store_true", help="Run a light CPU/RAM/disk benchmark and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Show optimization steps without executing them.")
    parser.add_argument("--force", action="store_true", help="Skip the elevation confirmation prompt.")
    parser.add_argument(
        "--profile", "-p", default="all", choices=optimizer.PROFILE_ORDER,
        help="Optimization profile: %s" % ", ".join(optimizer.PROFILE_ORDER),
    )
    parser.add_argument(
        "--language", "-l", default=None, metavar="CODE",
        help="Language code: %s" % ", ".join(LANGUAGE_ORDER),
    )
    parser.add_argument("--list-languages", action="store_true", help="List supported languages and exit.")
    parser.add_argument("--json", action="store_true", help="Emit inspection results as JSON.")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    args = parser.parse_args(argv)

    try:
        console = _make_console()
    except Exception as exc:
        print(
            "sys-opt requires the 'rich' package. Install with: pip install -r requirements.txt\n(%s)" % exc,
            file=sys.stderr,
        )
        return 1

    if args.language in LANGUAGES:
        language = args.language
    else:
        language = detect_system_language()
    t = build_translator(language)

    if args.list_languages:
        _print_languages(console)
        return 0
    rtl = LANGUAGES.get(language, {}).get("dir") == "rtl"
    if args.inspect:
        inspector.run(console, t, as_json=args.json, rtl=rtl)
        return 0
    if args.optimize:
        return optimizer.run(console, t, dry_run=args.dry_run, force=args.force, profile=args.profile)
    if args.suite:
        inspector.run(console, t, as_json=args.json, rtl=rtl)
        return optimizer.run(console, t, dry_run=args.dry_run, force=args.force, profile=args.profile)
    if args.benchmark:
        return benchmark.run(console, t, as_json=args.json)

    if not sys.stdin.isatty():
        _print_languages(console)
        console.print(
            "[dim]Non-interactive terminal: pass --inspect, --optimize, --suite, --benchmark or --list-languages.[/]"
        )
        return 0

    console.print(
        "[dim]%s: %s %s[/]" % (t("lang_detected"), LANGUAGES[language]["flag"], LANGUAGES[language]["native"])
    )
    return _interactive(console, language)


if __name__ == "__main__":
    sys.exit(main())
