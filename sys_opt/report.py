# -*- coding: utf-8 -*-
"""HTML performance report: full system specs + before/after benchmark results.

Writes a self-contained HTML file (inline CSS, no external assets) to
``~/.sys-opt/reports/`` and opens it in the default browser. Every failure
degrades to a console message instead of raising (zero-crash policy).

Flow:
- ``--benchmark --report``  -> benchmark (with the ``--compare`` baseline
  flow) then an HTML report with all specs + the latest two runs.
- ``--optimize --report``   -> complete benchmark BEFORE, optimize, complete
  benchmark AFTER, then an HTML report comparing before vs after — so the
  gain (or regression) of the optimization is visible at a glance.
"""

import html
import time
import webbrowser

from rich.panel import Panel

from . import benchmark, inspector, optimizer
from .utils import config_dir


def _esc(value):
    """HTML-escape a value for safe embedding in the report."""
    return html.escape("" if value is None else str(value), quote=True)


def _collect_sections(t):
    """Snapshot the full system inspection (localized) for the report."""
    try:
        return inspector.collect(t)
    except Exception:  # zero-crash policy
        return []


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def _render_sections(t, sections):
    """Render inspection sections (kv + table) as HTML cards."""
    blocks = []
    for section in sections:
        if section["type"] == "kv":
            rows = "".join(
                "<div class='kv'><dt>%s</dt><dd>%s</dd></div>"
                % (_esc(t(key)), _esc(value))
                for key, value in section["rows"]
            )
            blocks.append(
                "<section class='card'><h3>%s</h3><dl>%s</dl></section>"
                % (_esc(section["title"]), rows)
            )
        else:
            head = "".join("<th>%s</th>" % _esc(header) for header in section["headers"])
            rows = "".join(
                "<tr>%s</tr>"
                % "".join("<td>%s</td>" % _esc(cell) for cell in row)
                for row in section["rows"]
            )
            blocks.append(
                "<section class='card'><h3>%s</h3><table><thead><tr>%s</tr></thead>"
                "<tbody>%s</tbody></table></section>"
                % (_esc(section["title"]), head, rows)
            )
    return "\n".join(blocks)


def _fmt_metric(fmt, value):
    """Format one metric value; 'N/A' for missing/zero values."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return _esc("N/A")
    if value <= 0:
        return _esc("N/A")
    return _esc(fmt % value)


def _delta_html(delta):
    """Color-coded Δ cell: green up, red down, dash when not available."""
    if delta is None:
        return '<span class="muted">—</span>'
    color = "up" if delta >= 0 else "down"
    sign = "+" if delta >= 0 else ""
    return '<span class="%s">%s%.1f%%</span>' % (color, sign, delta)


def _render_benchmark(t, before, after):
    """Render the before/after benchmark comparison as an HTML table."""
    metrics = [
        ("benchmark_cpu", "cpu_mops", "%.2f M ops/s"),
        ("benchmark_ram", "ram_mbps", "%.0f MB/s"),
        ("benchmark_disk_write", "disk_write_mbps", "%.0f MB/s"),
        ("benchmark_disk_read", "disk_read_mbps", "%.0f MB/s"),
        ("benchmark_elapsed", "elapsed_seconds", "%.2f s"),
    ]
    if not before and not after:
        return '<p class="muted">%s</p>' % _esc(t("report_no_data"))
    rows = []
    for label_key, result_key, fmt in metrics:
        label = _esc(t(label_key))
        before_val = _fmt_metric(fmt, (before or {}).get(result_key))
        after_val = _fmt_metric(fmt, (after or {}).get(result_key))
        delta = benchmark._delta_pct(
            (after or {}).get(result_key), (before or {}).get(result_key)
        )
        rows.append(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (label, before_val, after_val, _delta_html(delta))
        )
    verdict = ""
    if after:
        try:
            verdict = (
                '<p class="verdict">%s: <strong>%s</strong></p>'
                % (_esc(t("report_verdict")), _esc(t(benchmark._verdict(after))))
            )
        except Exception:  # zero-crash policy
            verdict = ""
    return (
        "<table><thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead>"
        "<tbody>%s</tbody></table>%s"
        % (
            _esc(t("report_metric")),
            _esc(t("report_before")),
            _esc(t("report_after")),
            _esc(t("report_delta")),
            "\n".join(rows),
            verdict,
        )
    )


_CSS = """\
* { box-sizing: border-box; }
body { margin:0; font-family:'Segoe UI', system-ui, -apple-system, Roboto, Arial, sans-serif;
  background: linear-gradient(160deg,#0b1020 0%,#131a33 55%,#0e1526 100%); color:#e8ecf8; min-height:100vh; }
.wrap { max-width: 960px; margin: 0 auto; padding: 32px 20px 60px; }
.hero { text-align:center; padding: 28px 0 20px; }
.hero h1 { font-size: 15px; letter-spacing: 6px; text-transform: uppercase; color:#7ee0a3; margin:0; }
.hero h2 { font-size: 30px; margin: 8px 0 6px; background: linear-gradient(90deg,#7ee0a3,#4cc9f0);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.meta { color:#8a93b0; font-size: 13px; }
.card { background: rgba(255,255,255,.045); border: 1px solid rgba(255,255,255,.09);
  border-radius: 14px; padding: 20px 22px; margin: 18px 0; box-shadow: 0 8px 24px rgba(0,0,0,.25); }
.card h3 { margin: 0 0 14px; font-size: 17px; color:#9fd8ff; }
dl { display:grid; grid-template-columns: 1fr 1fr; gap: 10px 22px; margin:0; }
.kv dt { color:#8a93b0; font-size: 13px; }
.kv dd { margin:0; font-weight:600; font-size:14px; word-break: break-word; }
table { width:100%; border-collapse: collapse; font-size:14px; }
th { text-align:left; color:#8a93b0; font-weight:600; font-size:12px;
  text-transform:uppercase; letter-spacing:1px; padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.12); }
td { padding:9px 10px; border-bottom:1px solid rgba(255,255,255,.05); }
.up { color:#7ee0a3; font-weight:700; }
.down { color:#ff7a7a; font-weight:700; }
.muted { color:#8a93b0; }
.verdict { margin-top:14px; font-size:15px; padding:12px 14px; background:rgba(126,224,163,.08); border-radius:10px; }
.verdict strong { color:#7ee0a3; }
footer { text-align:center; color:#5b6480; font-size:12px; margin-top:30px; }
@media (max-width: 640px) { dl { grid-template-columns: 1fr; } .wrap { padding: 18px 12px 40px; } }
"""

_TEMPLATE = """\
<!DOCTYPE html>
<html lang="@@LANG@@" dir="@@DIR@@">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ — sys-opt</title>
<style>
@@CSS@@
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>🛠️ sys-opt</h1>
    <h2>@@TITLE@@</h2>
    <p class="meta">@@GENERATED@@ · @@NOW@@</p>
  </header>
  <main>
    @@SPECS@@
    <section class="card">
      <h3>📊 @@BENCH_LABEL@@</h3>
      @@BENCH@@
    </section>
  </main>
  <footer>sys-opt · github.com/Leo-Galli/sys-opt</footer>
</div>
</body>
</html>
"""


def build_html(t, language="en", before=None, after=None, sections=None, rtl=False):
    """Build a self-contained HTML page: specs + before/after benchmark."""
    sections = _collect_sections(t) if sections is None else sections
    replacements = {
        "@@LANG@@": _esc(language),
        "@@DIR@@": "rtl" if rtl else "ltr",
        "@@TITLE@@": _esc(t("report_title")),
        "@@GENERATED@@": _esc(t("report_generated")),
        "@@NOW@@": _esc(time.strftime("%Y-%m-%d %H:%M:%S")),
        "@@BENCH_LABEL@@": _esc(t("report_benchmark")),
        "@@CSS@@": _CSS,
        "@@SPECS@@": _render_sections(t, sections),
        "@@BENCH@@": _render_benchmark(t, before, after),
    }
    page = _TEMPLATE
    for token, value in replacements.items():
        page = page.replace(token, value)
    return page


# --------------------------------------------------------------------------- #
# Write + open
# --------------------------------------------------------------------------- #
def write_report(t, before=None, after=None, base=None, language="en", rtl=False):
    """Write the HTML report to ~/.sys-opt/reports/; returns its Path."""
    directory = config_dir(base) / "reports"
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception:  # zero-crash policy
        directory = None
    if directory is None:
        return None
    name = "sys-opt-report-%s.html" % time.strftime("%Y%m%d-%H%M%S")
    path = directory / name
    try:
        path.write_text(
            build_html(t, language=language, before=before, after=after, rtl=rtl),
            encoding="utf-8",
        )
        return path
    except Exception:  # zero-crash policy
        return None


def open_report(path):
    """Open the report in the default browser; True when launched."""
    try:
        return bool(webbrowser.open(path.resolve().as_uri()))
    except Exception:  # zero-crash policy
        return False


def _announce(console, t, path, opened):
    console.print()
    console.print("[bold green]%s[/]" % t("report_saved"))
    if path is not None:
        console.print("[dim]%s[/]" % (t("report_path") % str(path)))
    if not opened:
        console.print("[yellow]%s[/]" % t("report_open_failed"))


# --------------------------------------------------------------------------- #
# CLI orchestration
# --------------------------------------------------------------------------- #
def run_benchmark_report(console, t, base=None, language="en", rtl=False):
    """``--benchmark --report``: benchmark (baseline flow) + HTML report.

    The report includes all system specs and the before/after comparison of
    the last two saved runs (previous baseline vs this run).
    """
    rc = benchmark.run(console, t, compare=True, base=base)
    history = benchmark.load_history(base=base)
    after = history[-1].get("results") if history else None
    before = history[-2].get("results") if len(history) >= 2 else None
    path = write_report(t, before=before, after=after, base=base, language=language, rtl=rtl)
    _announce(console, t, path, open_report(path) if path is not None else False)
    return rc


def run_optimize_report(console, t, dry_run=False, force=False, profile="all",
                        base=None, language="en", rtl=False):
    """``--optimize --report``: complete benchmark before, optimize, complete
    benchmark after, then an HTML report comparing the two runs."""
    console.print()
    console.print(Panel("[bold cyan]%s[/]" % t("report_before_saved"), border_style="cyan"))
    benchmark.run(console, t, compare=True, base=base)
    console.print()
    rc = optimizer.run(console, t, dry_run=dry_run, force=force, profile=profile)
    console.print()
    console.print(Panel("[bold cyan]%s[/]" % t("report_after_saved"), border_style="cyan"))
    benchmark.run(console, t, compare=True, base=base)
    history = benchmark.load_history(base=base)
    after = history[-1].get("results") if history else None
    before = history[-2].get("results") if len(history) >= 2 else None
    path = write_report(t, before=before, after=after, base=base, language=language, rtl=rtl)
    _announce(console, t, path, open_report(path) if path is not None else False)
    return rc
