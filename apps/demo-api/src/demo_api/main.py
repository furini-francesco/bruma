from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlsplit

from .health import get_health_status


def create_app() -> dict[str, Any]:
    return {
        "name": "bruma-demo-api",
        "status": "ok",
        "version": "0.1.0",
        "health": get_health_status(),
    }


def render_metrics() -> str:
    return "\n".join(
        [
            "# HELP bruma_demo_api_up Whether the demo API is running.",
            "# TYPE bruma_demo_api_up gauge",
            "bruma_demo_api_up 1",
            "",
        ]
    )


class DemoAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlsplit(self.path).path

        if path == "/health":
            body = json.dumps(get_health_status()).encode("utf-8")
            content_type = "application/json; charset=utf-8"
            status = 200
        elif path == "/metrics":
            body = render_metrics().encode("utf-8")
            content_type = "text/plain; version=0.0.4; charset=utf-8"
            status = 200
        else:
            body = b'{"error":"not found"}'
            content_type = "application/json; charset=utf-8"
            status = 404

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", 8000), DemoAPIHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()