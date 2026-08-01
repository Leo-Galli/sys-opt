# -*- coding: utf-8 -*-
"""File benchmark through the browser: upload, detect, execute, measure.

Starts a local HTTP server bound to 127.0.0.1, opens the default browser on
an upload page, saves the uploaded file to a private temp directory,
recognizes its extension (.py / .c / .cpp / .exe / .sh / .go / .rs / .js /
.jar / .bat ...), compiles it when needed and executes it with a hard
timeout, then reports wall time, CPU time, exit code and output size.

SECURITY: sys-opt does NOT inspect the file content — it executes it. The
server is bound to loopback only, runs are timeout-bounded, the file lives
in a fresh temp directory that is removed afterwards, and the page carries
a prominent warning so this is never surprising.
"""

import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from rich.panel import Panel

#: Per-run hard timeout (seconds): protects the machine from runaway code.
_DEFAULT_TIMEOUT = 30
#: Maximum accepted upload size (bytes).
_MAX_BYTES = 20 * 1024 * 1024
#: How many ports to try when the requested one is busy.
_PORT_TRIES = 20


def _which(*names):
    """First executable found on PATH, or None."""
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def _plan(filename):
    """Return (kind_key, compile_argv, run_argv) for a filename.

    ``compile_argv`` is None for interpreted/executable files. Returns
    ``(kind_key, None, None)`` when the required tool is missing, and
    ``None`` when the extension is unsupported.
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".py":
        return "filebench_kind_python", None, [sys.executable, filename]
    if ext in (".c", ".cc", ".cpp", ".cxx"):
        compiler = _which("cc", "gcc", "clang")
        if not compiler:
            return "filebench_kind_c", None, None
        out = "a.exe" if os.name == "nt" else "a.out"
        return "filebench_kind_c", [compiler, filename, "-O2", "-o", out], [os.path.join(".", out)]
    if ext == ".rs":
        rustc = _which("rustc")
        if not rustc:
            return "filebench_kind_rust", None, None
        out = "a.exe" if os.name == "nt" else "a.out"
        return "filebench_kind_rust", [rustc, filename, "-O", "-o", out], [os.path.join(".", out)]
    if ext == ".go":
        go = _which("go")
        if not go:
            return "filebench_kind_go", None, None
        return "filebench_kind_go", None, [go, "run", filename]
    if ext == ".exe":
        run_target = filename if os.name == "nt" else os.path.join(".", filename)
        return "filebench_kind_exe", None, [run_target]
    if ext == ".sh":
        shell = _which("sh", "bash")
        if not shell:
            return "filebench_kind_shell", None, None
        return "filebench_kind_shell", None, [shell, filename]
    if os.name == "nt" and ext in (".bat", ".cmd"):
        return "filebench_kind_batch", None, ["cmd", "/c", filename]
    if ext == ".js":
        node = _which("node", "nodejs")
        if not node:
            return "filebench_kind_js", None, None
        return "filebench_kind_js", None, [node, filename]
    if ext == ".jar":
        java = _which("java")
        if not java:
            return "filebench_kind_jar", None, None
        return "filebench_kind_jar", None, [java, "-jar", filename]
    if ext == ".php":
        php = _which("php")
        if not php:
            return "filebench_kind_php", None, None
        return "filebench_kind_php", None, [php, filename]
    if ext == ".rb":
        ruby = _which("ruby")
        if not ruby:
            return "filebench_kind_ruby", None, None
        return "filebench_kind_ruby", None, [ruby, filename]
    return None


def _children_cpu():
    """Cumulative CPU seconds used by finished child processes (POSIX)."""
    try:
        import resource

        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        return usage.ru_utime + usage.ru_stime
    except Exception:  # pragma: no cover - non-POSIX / restricted
        return None


def _timed_run(argv, cwd, timeout):
    """Run one command with a timeout; returns a measured result dict."""
    started = time.perf_counter()
    cpu_before = _children_cpu()
    try:
        proc = subprocess.run(
            argv,
            cwd=cwd,
            timeout=timeout,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        returncode = proc.returncode
        output = (proc.stdout or "") + (proc.stderr or "")
        timed_out = False
    except subprocess.TimeoutExpired:
        returncode = -1
        output = ""
        timed_out = True
    except Exception as exc:  # zero-crash policy: never let a launch error escape
        returncode = -2
        output = str(exc)
        timed_out = False
    wall = time.perf_counter() - started
    cpu = None
    if cpu_before is not None:
        cpu_after = _children_cpu()
        if cpu_after is not None:
            cpu = max(0.0, cpu_after - cpu_before)
    return {
        "returncode": returncode,
        "wall": wall,
        "cpu": cpu,
        "output": output,
        "timed_out": timed_out,
    }


def _handle_payload(t, payload, timeout=_DEFAULT_TIMEOUT, max_bytes=_MAX_BYTES):
    """Benchmark one uploaded file; returns a JSON-serializable dict."""
    filename = os.path.basename(str(payload.get("filename", "")) or "")
    content_b64 = payload.get("content", "")
    if not filename or not content_b64:
        return {"error": t("filebench_no_file")}
    try:
        content = base64.b64decode(content_b64)
    except Exception:  # zero-crash policy
        return {"error": t("filebench_error")}
    if len(content) > max_bytes:
        return {"error": t("filebench_too_large") % (max_bytes // (1024 * 1024))}
    plan = _plan(filename)
    if plan is None:
        return {"error": t("filebench_unknown"), "filename": filename}
    kind_key, compile_argv, run_argv = plan
    if compile_argv is None and run_argv is None:
        return {"error": t("filebench_no_compiler"), "kind": t(kind_key), "filename": filename}

    workdir = tempfile.mkdtemp(prefix="sysopt-filebench-")
    try:
        target = os.path.join(workdir, filename)
        with open(target, "wb") as handle:
            handle.write(content)
        if os.name != "nt":
            os.chmod(target, 0o755)
        if compile_argv:
            compiled = _timed_run(compile_argv, workdir, timeout)
            if compiled["returncode"] != 0:
                return {
                    "error": t("filebench_compile_failed"),
                    "kind": t(kind_key),
                    "filename": filename,
                    "output": compiled["output"][-2000:],
                }
        info = _timed_run(run_argv, workdir, timeout)
        return {
            "ok": info["returncode"] == 0 and not info["timed_out"],
            "kind": t(kind_key),
            "filename": filename,
            "wall_seconds": round(info["wall"], 3),
            "cpu_seconds": round(info["cpu"], 3) if info.get("cpu") is not None else None,
            "returncode": info["returncode"],
            "timed_out": info["timed_out"],
            "output_size": len(info["output"].encode("utf-8", "replace")),
            "preview": info["output"][-2000:],
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Upload page
# --------------------------------------------------------------------------- #
_PAGE_CSS = """\
* { box-sizing: border-box; }
body { margin:0; font-family:'Segoe UI', system-ui, -apple-system, Roboto, Arial, sans-serif;
  background: linear-gradient(160deg,#0b1020 0%,#131a33 55%,#0e1526 100%); color:#e8ecf8; min-height:100vh; }
.wrap { max-width: 760px; margin: 0 auto; padding: 32px 20px 60px; }
.hero { text-align:center; padding: 20px 0; }
.hero h1 { font-size: 15px; letter-spacing: 6px; text-transform: uppercase; color:#7ee0a3; margin:0; }
.hero h2 { font-size: 28px; margin: 8px 0 6px; background: linear-gradient(90deg,#7ee0a3,#4cc9f0);
  -webkit-background-clip: text; background-clip: text; color: transparent; }
.warn { background: rgba(255,90,90,.12); border: 1px solid rgba(255,110,110,.45); border-radius: 12px;
  padding: 14px 16px; margin: 18px 0; }
.warn h3 { margin: 0 0 6px; color:#ff8a8a; font-size: 15px; }
.warn p { margin: 0; color:#ffd0d0; font-size: 13px; line-height: 1.5; }
.card { background: rgba(255,255,255,.045); border: 1px solid rgba(255,255,255,.09);
  border-radius: 14px; padding: 20px 22px; margin: 18px 0; box-shadow: 0 8px 24px rgba(0,0,0,.25); }
.drop { border: 2px dashed rgba(126,224,163,.5); border-radius: 12px; padding: 34px 20px; text-align:center;
  cursor: pointer; transition: background .2s, border-color .2s; }
.drop.over { background: rgba(126,224,163,.1); border-color:#7ee0a3; }
.drop .big { font-size: 40px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; justify-content: center; }
.chip { background: rgba(126,224,163,.12); border: 1px solid rgba(126,224,163,.35); color:#9ff0bd;
  font-size: 12px; padding: 4px 10px; border-radius: 999px; font-family: monospace; }
button.primary { display: block; width: 100%; margin-top: 14px; padding: 13px;
  font-size: 16px; font-weight: 700;
  border: none; border-radius: 10px; background: linear-gradient(90deg,#7ee0a3,#4cc9f0);
  color:#0b1020; cursor: pointer; }
button.primary:disabled { opacity: .5; cursor: wait; }
#fileInfo { text-align:center; margin-top: 10px; color:#9fd8ff; font-size: 14px; min-height: 20px; }
table { width:100%; border-collapse: collapse; font-size:14px; margin-top: 6px; }
th { text-align:left; color:#8a93b0; font-weight:600; font-size:12px; text-transform:uppercase;
  letter-spacing:1px; padding:8px 10px; border-bottom:1px solid rgba(255,255,255,.12); }
td { padding:9px 10px; border-bottom:1px solid rgba(255,255,255,.05); }
.ok { color:#7ee0a3; font-weight:700; }
.bad { color:#ff7a7a; font-weight:700; }
pre { background: rgba(0,0,0,.35); border-radius: 8px; padding: 12px; overflow-x: auto;
  max-height: 240px; font-size: 12px; color:#cfe3ff; white-space: pre-wrap; word-break: break-word; }
.muted { color:#8a93b0; }
footer { text-align:center; color:#5b6480; font-size:12px; margin-top:30px; }
"""


def build_page(t):
    """Self-contained upload page (localized), served at ``/``."""
    js = {
        "upload": t("filebench_upload"),
        "drop": t("filebench_drop"),
        "run": t("filebench_run"),
        "running": t("filebench_running"),
        "noFile": t("filebench_no_file"),
        "extension": t("filebench_extension"),
        "wall": t("filebench_wall"),
        "cpu": t("filebench_cpu"),
        "exit": t("filebench_exit"),
        "stdout": t("filebench_stdout"),
        "ok": t("filebench_ok"),
        "error": t("filebench_error"),
        "timeout": t("filebench_timeout"),
        "results": t("filebench_results"),
        "preview": t("filebench_preview"),
    }
    js_json = json.dumps(js, ensure_ascii=False)
    chips = " ".join(
        "<span class='chip'>%s</span>"
        % ext
        for ext in (".py", ".c", ".cpp", ".rs", ".go", ".exe", ".sh", ".js", ".jar", ".php", ".rb")
    )
    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s — sys-opt</title>
<style>
%s
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>🛠️ sys-opt</h1>
    <h2>%s</h2>
  </header>
  <div class="warn">
    <h3>⚠️ %s</h3>
    <p>%s</p>
  </div>
  <div class="card">
    <div class="drop" id="drop">
      <div class="big">📁</div>
      <p><strong>%s</strong><br><span class="muted">%s</span></p>
      <input type="file" id="file" hidden>
    </div>
    <div id="fileInfo"></div>
    <button class="primary" id="runBtn" disabled>🚀 %s</button>
    <div class="chips">%s</div>
  </div>
  <div class="card" id="resultsCard" hidden>
    <h3 style="margin:0 0 12px;color:#9fd8ff">📊 %s</h3>
    <div id="results"></div>
  </div>
  <footer>sys-opt · github.com/Leo-Galli/sys-opt</footer>
</div>
<script>
const I18N = %s;
const drop = document.getElementById('drop');
const fileInput = document.getElementById('file');
const fileInfo = document.getElementById('fileInfo');
const runBtn = document.getElementById('runBtn');
const resultsCard = document.getElementById('resultsCard');
const results = document.getElementById('results');
let selectedFile = null;

drop.addEventListener('click', () => fileInput.click());
drop.addEventListener('dragover', (e) => { e.preventDefault(); drop.classList.add('over'); });
drop.addEventListener('dragleave', () => drop.classList.remove('over'));
drop.addEventListener('drop', (e) => {
  e.preventDefault();
  drop.classList.remove('over');
  if (e.dataTransfer.files && e.dataTransfer.files[0]) pick(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files && fileInput.files[0]) pick(fileInput.files[0]); });

function pick(file) {
  selectedFile = file;
  fileInfo.textContent = '📄 ' + file.name + ' · ' + (file.size / 1024).toFixed(1) + ' KB';
  runBtn.disabled = false;
}

runBtn.addEventListener('click', async () => {
  if (!selectedFile) { alert(I18N.noFile); return; }
  runBtn.disabled = true;
  runBtn.textContent = '⏳ ' + I18N.running;
  try {
    const b64 = await readFile(selectedFile);
    const resp = await fetch('/api/benchmark', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename: selectedFile.name, content: b64 })
    });
    const data = await resp.json();
    render(data);
  } catch (err) {
    render({ error: String(err) });
  } finally {
    runBtn.disabled = false;
    runBtn.textContent = '🚀 ' + I18N.run;
  }
});

function readFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(',')[1] || '');
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function render(data) {
  resultsCard.hidden = false;
  if (data.error) {
    results.innerHTML = '<p class="bad">⚠️ ' + I18N.error + ': ' + esc(data.error) + '</p>';
    return;
  }
  const status = data.ok
    ? '<span class="ok">✔ ' + I18N.ok + '</span>'
    : '<span class="bad">✖ ' + I18N.error + '</span>';
  const wall = data.timed_out ? I18N.timeout : data.wall_seconds + ' s';
  const rows = [
    [I18N.extension, esc(data.kind)],
    [I18N.wall, wall],
    [I18N.cpu, (data.cpu_seconds === null ? '—' : data.cpu_seconds + ' s')],
    [I18N.exit, data.returncode],
    [I18N.stdout, data.output_size + ' B'],
  ].map(([k, v]) => '<tr><td>' + k + '</td><td>' + v + '</td></tr>').join('');
  const preview = data.preview ? '<pre>' + esc(data.preview) + '</pre>' : '';
  results.innerHTML = '<p>' + status + ' — ' + esc(data.filename) + '</p>'
    + '<table><tbody>' + rows + '</tbody></table>' + preview;
}

function esc(text) {
  return String(text).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}
</script>
</body>
</html>
""" % (
        t("report_title"),
        _PAGE_CSS,
        t("filebench_header"),
        t("filebench_warning_title"),
        t("filebench_warning_body"),
        t("filebench_upload"),
        t("filebench_drop"),
        t("filebench_run"),
        chips,
        t("filebench_results"),
        js_json,
    )
    return page


# --------------------------------------------------------------------------- #
# Server
# --------------------------------------------------------------------------- #
def make_handler(t, timeout=_DEFAULT_TIMEOUT, max_bytes=_MAX_BYTES):
    """Build the HTTP handler class bound to a specific translator."""

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # silence request logs
            pass

        def _send(self, code, content_type, body):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, obj):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self._send(200, "application/json; charset=utf-8", body)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                page = build_page(t)
                self._send(200, "text/html; charset=utf-8", page.encode("utf-8"))
            else:
                self._send(404, "text/plain; charset=utf-8", b"not found")

        def do_POST(self):
            if self.path != "/api/benchmark":
                self._send(404, "text/plain; charset=utf-8", b"not found")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except (TypeError, ValueError):  # zero-crash policy
                length = 0
            if length <= 0:
                # No (or bogus) body: answer with the friendly empty-state error.
                self._send_json({"error": t("filebench_no_file")})
                return
            if length > max_bytes * 2:
                # Too large to even buffer: answer with the too-large error
                # instead of reading it (base64 overhead ~33% is already in
                # max_bytes * 2 headroom, so real limits still hit this).
                self._send_json(
                    {"error": t("filebench_too_large") % (max_bytes // (1024 * 1024))}
                )
                return
            payload = {}
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except Exception:  # zero-crash policy
                payload = {}
            result = _handle_payload(t, payload, timeout=timeout, max_bytes=max_bytes)
            self._send_json(result)

    return Handler


def run(console, t, port=8765, timeout=_DEFAULT_TIMEOUT):
    """Start the loopback file-benchmark server and open the browser.

    Blocks serving until Ctrl+C; returns 0 on clean shutdown.
    """
    handler = make_handler(t, timeout=timeout)
    server = None
    for candidate in range(port, port + _PORT_TRIES):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), handler)
            break
        except OSError:
            continue
    if server is None:
        console.print("[bold red]%s[/]" % (t("filebench_port_busy") % port))
        return 1
    actual_port = server.server_address[1]
    url = "http://127.0.0.1:%d/" % actual_port
    console.print()
    console.print(
        Panel(
            "[bold green]%s[/] — %s" % (t("filebench_header"), url),
            border_style="green",
        )
    )
    console.print("[bold yellow]⚠ %s[/]" % t("filebench_warning_title"))
    console.print("[yellow]%s[/]" % t("filebench_warning_body"))
    console.print("[dim]%s[/]" % t("filebench_stop"))
    try:
        webbrowser.open(url)
    except Exception:  # zero-crash policy
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0
