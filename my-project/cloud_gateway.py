#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from cloud_gateway_app.config import GatewayConfig, load_gateway_config
from cloud_gateway_app.proxy import proxy_request
from cloud_gateway_app.routing import Upstream
from cloud_gateway_app.static_site import serve_static_file
from cloud_gateway_app.visitors import IPVisitorCounter

BOOT_CONFIG = load_gateway_config()


class GatewayHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    visitor_counter: IPVisitorCounter | None = None

    @property
    def config(self) -> GatewayConfig:
        """Expose typed configuration stored on the HTTP server."""
        return self.server.config

    def _get_client_ip(self) -> str:
        """Extract real client IP, handling Cloudflare headers."""
        if "CF-Connecting-IP" in self.headers:
            return self.headers["CF-Connecting-IP"]
        if "X-Forwarded-For" in self.headers:
            return self.headers["X-Forwarded-For"].split(",")[0].strip()
        return self.client_address[0]

    def _send_json_response(self, status: int, data: dict) -> None:
        """Send JSON response with appropriate headers."""
        response_body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(response_body)

    def _handle_visitor_count(self) -> bool:
        """Handle /api/visitor-count requests. Return True if handled."""
        if self.path == "/api/visitor-count":
            if self.visitor_counter is None:
                self._send_json_response(500, {"error": "Counter not initialized"})
                return True

            if self.command == "GET":
                client_ip = self._get_client_ip()
                count = self.visitor_counter.record_visitor(client_ip)
                self._send_json_response(200, {"count": count, "success": True})
                return True
            if self.command == "OPTIONS":
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()
                return True
        return False

    def _serve_static_file(self) -> bool:
        """Serve files from the built static site when available."""
        return serve_static_file(self, self.config.site_dir, self.path)

    def _proxy(self) -> None:
        config = self.config
        proxy_request(
            self,
            ai_upstream=Upstream(config.ai_host, config.ai_port, ""),
            drive_upstream=Upstream(config.drive_host, config.drive_port, config.drive_prefix),
        )

    def do_GET(self) -> None:
        if self._handle_visitor_count():
            return

        parsed = urlsplit(self.path)
        drive_prefix = self.config.drive_prefix
        if drive_prefix and (parsed.path == drive_prefix or parsed.path.startswith(drive_prefix + "/")):
            self._proxy()
            return

        if self._serve_static_file():
            return

        self._proxy()

    def do_POST(self) -> None:
        self._proxy()

    def do_PUT(self) -> None:
        self._proxy()

    def do_PATCH(self) -> None:
        self._proxy()

    def do_DELETE(self) -> None:
        self._proxy()

    def do_OPTIONS(self) -> None:
        if self._handle_visitor_count():
            return
        self._proxy()

    def do_HEAD(self) -> None:
        self._proxy()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Gateway for LobeChat, Cloud Drive, and Website")
    parser.add_argument("--host", default=BOOT_CONFIG.host)
    parser.add_argument("--port", default=BOOT_CONFIG.port, type=int)
    parser.add_argument("--ai-host", default=BOOT_CONFIG.ai_host)
    parser.add_argument("--ai-port", default=BOOT_CONFIG.ai_port, type=int)
    parser.add_argument("--drive-host", default=BOOT_CONFIG.drive_host)
    parser.add_argument("--drive-port", default=BOOT_CONFIG.drive_port, type=int)
    parser.add_argument("--drive-prefix", default=BOOT_CONFIG.drive_prefix)
    parser.add_argument("--site-dir", default=str(BOOT_CONFIG.site_dir))
    parser.add_argument("--visitor-data-file", default=str(BOOT_CONFIG.visitor_data_file))
    args = parser.parse_args()

    config = load_gateway_config(
        host=args.host,
        port=args.port,
        ai_host=args.ai_host,
        ai_port=args.ai_port,
        drive_host=args.drive_host,
        drive_port=args.drive_port,
        drive_prefix=args.drive_prefix,
        site_dir=args.site_dir,
        visitor_data_file=args.visitor_data_file,
    )
    counter = IPVisitorCounter(config.visitor_data_file)

    server = ThreadingHTTPServer((args.host, args.port), GatewayHandler)
    server.config = config
    GatewayHandler.visitor_counter = counter

    print(f"Gateway listening on http://{args.host}:{args.port}")
    print(f"AI upstream: http://{config.ai_host}:{config.ai_port}")
    print(f"Cloud Drive upstream: http://{config.drive_host}:{config.drive_port}{config.drive_prefix}")
    print(f"Static site directory: {config.site_dir}")
    print(f"Visitor counter: {counter.get_count()} unique visitors")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
