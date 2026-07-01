from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ..attacks.schema import AttackSample


@dataclass(frozen=True)
class RunningProxy:
    server: ThreadingHTTPServer
    thread: threading.Thread

    @property
    def url(self) -> str:
        host, port = self.server.server_address
        return f"http://{host}:{port}"


def _handler(service):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return

        def _json(self, status, payload):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/health":
                self._json(200, {"status": "ok"})
            else:
                self._json(404, {"error": "not found"})

        def do_POST(self):
            if self.path != "/v1/chat/completions":
                self._json(404, {"error": "not found"})
                return
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            mode = self.headers.get("X-CodeGuarder-Mode", "P")
            metadata = payload.pop("_codeguarder", {})
            sample_data = metadata.get("sample") if isinstance(metadata, dict) else None
            sample = AttackSample.from_dict(sample_data) if sample_data else None
            result = service.process(payload, mode, sample=sample)
            self._json(200, result.response)

    return Handler


@contextmanager
def running_proxy(service):
    server = ThreadingHTTPServer(("127.0.0.1", 0), _handler(service))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    proxy = RunningProxy(server, thread)
    try:
        yield proxy
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
