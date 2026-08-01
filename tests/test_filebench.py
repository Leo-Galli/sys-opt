# -*- coding: utf-8 -*-
"""Tests for the browser file-benchmark module (--benchmark-file)."""

import base64
import http.client
import json
import threading
import unittest
import urllib.request
from unittest import mock

from sys_opt import filebench
from sys_opt.i18n.languages import build_translator


def _start_server(handler):
    """Start a loopback server on a free port; returns the server object."""
    server = filebench.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def _post_raw(port, headers):
    """POST /api/benchmark with explicit raw headers; returns (status, data)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.putrequest("POST", "/api/benchmark")
        for key, value in headers.items():
            conn.putheader(key, value)
        conn.endheaders()
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read().decode("utf-8"))
    finally:
        conn.close()


class TestFilebench(unittest.TestCase):
    def test_plan_python(self):
        kind, compile_argv, run_argv = filebench._plan("hello.py")
        self.assertEqual(kind, "filebench_kind_python")
        self.assertIsNone(compile_argv)
        self.assertEqual(run_argv, [filebench.sys.executable, "hello.py"])

    def test_plan_unknown(self):
        self.assertIsNone(filebench._plan("data.xyz"))

    def test_plan_c_without_compiler(self):
        with mock.patch("sys_opt.filebench.shutil.which", return_value=None):
            kind, compile_argv, run_argv = filebench._plan("hello.c")
        self.assertEqual(kind, "filebench_kind_c")
        self.assertIsNone(compile_argv)
        self.assertIsNone(run_argv)

    def test_handle_payload_python_runs(self):
        t = build_translator("en")
        content = base64.b64encode(b"print('hi from sys-opt')\n").decode("ascii")
        result = filebench._handle_payload(t, {"filename": "hello.py", "content": content})
        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("returncode"), 0)
        self.assertEqual(result.get("kind"), "Python")
        self.assertIn("hi from sys-opt", result.get("preview", ""))

    def test_handle_payload_unknown_extension(self):
        t = build_translator("en")
        content = base64.b64encode(b"junk").decode("ascii")
        result = filebench._handle_payload(t, {"filename": "file.xyz", "content": content})
        self.assertEqual(result.get("error"), t("filebench_unknown"))

    def test_handle_payload_no_file(self):
        t = build_translator("en")
        result = filebench._handle_payload(t, {})
        self.assertEqual(result.get("error"), t("filebench_no_file"))

    def test_handle_payload_too_large(self):
        t = build_translator("en")
        content = base64.b64encode(b"x" * 100).decode("ascii")
        result = filebench._handle_payload(
            t, {"filename": "a.py", "content": content}, max_bytes=10
        )
        self.assertIn("MB", result.get("error", ""))

    def test_handle_payload_timeout(self):
        t = build_translator("en")
        content = base64.b64encode(b"import time\ntime.sleep(5)\n").decode("ascii")
        result = filebench._handle_payload(
            t, {"filename": "slow.py", "content": content}, timeout=1
        )
        self.assertTrue(result.get("timed_out"))
        self.assertEqual(result.get("returncode"), -1)

    def test_build_page_contains_warning(self):
        t = build_translator("en")
        page = filebench.build_page(t)
        self.assertIn("Security Warning", page)
        self.assertIn("does NOT inspect", page)

    def test_handler_serves_page_and_benchmarks(self):
        t = build_translator("en")
        handler = filebench.make_handler(t)
        server = _start_server(handler)
        port = server.server_address[1]
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/" % port, timeout=10) as resp:
                body = resp.read().decode("utf-8")
                self.assertEqual(resp.status, 200)
                self.assertIn("File Benchmark", body)
            payload = json.dumps(
                {
                    "filename": "hello.py",
                    "content": base64.b64encode(b"print('from server')\n").decode("ascii"),
                }
            ).encode("utf-8")
            req = urllib.request.Request(
                "http://127.0.0.1:%d/api/benchmark" % port,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(data.get("ok"))
                self.assertEqual(data.get("kind"), "Python")
        finally:
            server.shutdown()
            server.server_close()

    def test_handler_post_empty_body_answers_no_file(self):
        """A POST with Content-Length 0 (no body) must answer the localized
        empty-state error, never read or hang (do_POST early return)."""
        t = build_translator("en")
        server = _start_server(filebench.make_handler(t))
        port = server.server_address[1]
        try:
            status, data = _post_raw(port, {"Content-Length": "0"})
            self.assertEqual(status, 200)
            self.assertEqual(data.get("error"), t("filebench_no_file"))
        finally:
            server.shutdown()
            server.server_close()

    def test_handler_post_huge_content_length_answers_too_large(self):
        """A POST declaring a Content-Length beyond the clamp must answer
        'file too large' immediately without buffering the body."""
        t = build_translator("en")
        server = _start_server(filebench.make_handler(t, max_bytes=1024))
        port = server.server_address[1]
        try:
            status, data = _post_raw(port, {"Content-Length": "999999999"})
            self.assertEqual(status, 200)
            self.assertIn("MB", data.get("error", ""))
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
