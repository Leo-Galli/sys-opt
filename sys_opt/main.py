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
from .utils import arrow_menu, load_config, save_config
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


def _choose_language(console, t, title_key="lang_prompt"):
    """Arrow-key language picker; returns a language code or None."""
    items = []
    for code in LANGUAGE_ORDER:
        meta = LANGUAGES[code]
        items.append("%s %s (%s)" % (meta["flag"], meta["native"], code))
    index = arrow_menu(console, t(title_key), items, hint=t("menu_arrow_hint"))
    if index is None:
        return None
    return LANGUAGE_ORDER[index]


def _main_menu(console, t):
    """Arrow-key main menu; returns 0-6 or None (exit / cancel)."""
    items = [
        "🔍 %s" % t("menu_inspect"),
        "🚀 %s" % t("menu_optimize"),
        "⚡ %s" % t("menu_suite"),
        "📊 %s" % t("menu_benchmark"),
        "💡 %s" % t("menu_suggest"),
        "🌐 %s" % t("menu_language"),
        "🚪 %s" % t("menu_exit"),
    ]
    return arrow_menu(console, t("menu_title"), items, hint=t("menu_arrow_hint"))


def _print_banner(console):
    """Print the ASCII-art brand banner (language-independent)."""
    from rich.panel import Panel
    from rich.text import Text

    console.print(Panel(Text(_SYS_OPT_BANNER, style="bold cyan"), border_style="cyan"))


def _choose_profile(console, t):
    """Arrow-key profile picker; falls back to 'all' on cancel."""
    items = [t(optimizer.PROFILE_LABEL_KEYS[code]) for code in optimizer.PROFILE_ORDER]
    index = arrow_menu(console, t("profile_prompt"), items, hint=t("menu_arrow_hint"))
    if index is None:
        return "all"
    return optimizer.PROFILE_ORDER[index]


def _pause(console, t):
    try:
        console.input(t("press_enter"))
    except Exception:
        pass


def _print_language_saved(console, t, language):
    meta = LANGUAGES[language]
    console.print(
        "[bold green]✓ %s: %s %s — %s[/]"
        % (t("lang_selected"), meta["flag"], meta["native"], t("lang_saved"))
    )


def _interactive(console, initial_language, first_run=False):
    language = initial_language
    t = build_translator(language)
    console.print()
    _print_banner(console)
    if first_run:
        console.print()
        console.print("[bold cyan]%s[/]" % t("lang_first_run"))
        picked = _choose_language(console, t)
        if picked:
            language = picked
            t = build_translator(language)
            save_config(language)
            console.print()
            _print_language_saved(console, t, language)
            _pause(console, t)
    while True:
        console.print()
        index = _main_menu(console, t)
        if index is None or index == 6:
            console.print()
            console.print("[bold green]%s[/]" % t("goodbye"))
            return 0
        if index == 0:
            inspector.run(console, t, rtl=LANGUAGES[language]["dir"] == "rtl")
            _pause(console, t)
        elif index == 1:
            optimizer.run(console, t, profile=_choose_profile(console, t))
            _pause(console, t)
        elif index == 2:
            profile = _choose_profile(console, t)
            inspector.run(console, t, rtl=LANGUAGES[language]["dir"] == "rtl")
            optimizer.run(console, t, profile=profile)
            _pause(console, t)
        elif index == 3:
            benchmark.run(console, t)
            _pause(console, t)
        elif index == 4:
            optimizer.suggest(console, t, profile=_choose_profile(console, t))
            _pause(console, t)
        elif index == 5:
            picked = _choose_language(console, t)
            if picked:
                language = picked
                t = build_translator(language)
                save_config(language)
                console.print()
                _print_language_saved(console, t, language)
            _pause(console, t)


def main(argv=None):
    _ensure_utf8_output()
    parser = argparse.ArgumentParser(
        prog="sys-opt",
        description="Universal Hardware Inspector & Multi-OS Optimizer (10+ languages).",
    )
    parser.add_argument("--inspect", action="store_true", help="Inspect hardware specs and exit.")
    parser.add_argument("--optimize", action="store_true", help="Run system optimization and exit.")
    parser.add_argument(
        "--suggest", action="store_true",
        help="Inspect the system and propose the most impactful optimizations "
        "(ranked by estimated FPS/performance effect); applies only after your confirmation. "
        "Combine with --optimize.",
    )
    parser.add_argument("--suite", action="store_true", help="Inspect then optimize, then exit.")
    parser.add_argument("--benchmark", action="store_true", help="Run a light CPU/RAM/disk benchmark and exit.")
    parser.add_argument(
        "--compare", action="store_true",
        help="With --benchmark: save the result in ~/.sys-opt and show the %% change vs the previous baseline.",
    )
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

    # Language resolution order: explicit --language > saved config > system detect.
    saved = load_config().get("language")
    if args.language in LANGUAGES:
        language = args.language
        from_config = False
    elif saved in LANGUAGES:
        language = saved
        from_config = True
    else:
        language = detect_system_language()
        from_config = False
    t = build_translator(language)

    if args.list_languages:
        _print_languages(console)
        return 0
    rtl = LANGUAGES.get(language, {}).get("dir") == "rtl"
    if args.inspect:
        inspector.run(console, t, as_json=args.json, rtl=rtl)
        return 0
    if args.suggest:
        return optimizer.suggest(console, t, dry_run=args.dry_run, force=args.force, profile=args.profile)
    if args.optimize:
        return optimizer.run(console, t, dry_run=args.dry_run, force=args.force, profile=args.profile)
    if args.suite:
        inspector.run(console, t, as_json=args.json, rtl=rtl)
        return optimizer.run(console, t, dry_run=args.dry_run, force=args.force, profile=args.profile)
    if args.benchmark:
        return benchmark.run(console, t, as_json=args.json, compare=args.compare)

    if not sys.stdin.isatty():
        _print_languages(console)
        console.print(
            "[dim]Non-interactive terminal: pass --inspect, --optimize, --suite, --benchmark or --list-languages.[/]"
        )
        return 0

    label_key = "lang_current" if from_config else "lang_detected"
    console.print(
        "[dim]%s: %s %s[/]" % (t(label_key), LANGUAGES[language]["flag"], LANGUAGES[language]["native"])
    )
    first_run = saved not in LANGUAGES and args.language not in LANGUAGES
    return _interactive(console, language, first_run=first_run)


if __name__ == "__main__":
    sys.exit(main())
