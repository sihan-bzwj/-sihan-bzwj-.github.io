#!/usr/bin/env python3

from __future__ import annotations

import argparse
import http.client
import json
import os
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}


class VisitorCounter:
    """Thread-safe visitor counter using file persistence."""
    def __init__(self, file_path: str = ".visitor_count"):
        self.file_path = Path(file_path)
        self.lock = threading.Lock()
        self._load()

    def _load(self) -> None:
        if self.file_path.exists():
            try:
                self.count = int(self.file_path.read_text().strip())
            except (ValueError, OSError):
                self.count = 0
        else:
            self.count = 0

    def _save(self) -> None:
        try:
            self.file_path.write_text(str(self.count))
        except OSError:
            pass

    def increment(self) -> int:
        with self.lock:
            self.count += 1
            self._save()
            return self.count

    def get(self) -> int:
        with self.lock:
            return self.count


@dataclass(frozen=True)
class Upstream:
    host: str
    port: int
    mount_prefix: str = ""


def normalize_mount_prefix(value: str) -> str:
    cleaned = "/" + value.strip("/")
    return "" if cleaned == "/" else cleaned


def choose_upstream(path: str, ai_upstream: Upstream, drive_upstream: Upstream) -> tuple[Upstream, str]:
    prefix = drive_upstream.mount_prefix
    if prefix and (path == prefix or path.startswith(prefix + "/")):
        stripped_path = path[len(prefix):] or "/"
        return drive_upstream, stripped_path
    return ai_upstream, path


def rewrite_location(location: str, upstream: Upstream) -> str:
    prefix = upstream.mount_prefix
    if not prefix:
        return location

    parsed = urlsplit(location)
    if parsed.scheme and parsed.netloc:
        if parsed.hostname in {upstream.host, "localhost", "127.0.0.1"} and (parsed.port in {None, upstream.port}):
            rewritten_path = parsed.path or "/"
            if rewritten_path == "/":
                rewritten_path = prefix + "/"
            elif rewritten_path.startswith("/"):
                rewritten_path = prefix + rewritten_path
            else:
                rewritten_path = prefix + "/" + rewritten_path
            return urlunsplit(("", "", rewritten_path, parsed.query, parsed.fragment))
        return location

    if location.startswith("/"):
        if location == "/":
            return prefix + "/"
        if location == prefix or location.startswith(prefix + "/"):
            return location
        return prefix + location

    return location


class GatewayHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    visitor_counter: VisitorCounter | None = None

    def _send_json_response(self, status: int, data: dict) -> None:
        """Send JSON response with appropriate headers."""
        response_body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response_body)

    def _handle_visitor_count(self) -> bool:
        """Handle /api/visitor-count requests. Return True if handled."""
        if self.path == "/api/visitor-count":
            if self.visitor_counter is None:
                self._send_json_response(500, {"error": "Counter not initialized"})
                return True

            if self.command == "GET":
                count = self.visitor_counter.increment()
                self._send_json_response(200, {"count": count, "success": True})
                return True
            elif self.command == "OPTIONS":
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
                self.end_headers()
                return True
        return False

    def _proxy(self) -> None:
        parsed = urlsplit(self.path)
        ai_upstream = Upstream(self.server.ai_host, self.server.ai_port, "")
        drive_upstream = Upstream(self.server.drive_host, self.server.drive_port, self.server.drive_prefix)
        upstream, upstream_path = choose_upstream(parsed.path, ai_upstream, drive_upstream)
        target_path = upstream_path if not parsed.query else f"{upstream_path}?{parsed.query}"

        headers: dict[str, str] = {}
        incoming_host = self.headers.get("Host")
        for key, value in self.headers.items():
            if key.lower() in HOP_BY_HOP_HEADERS or key.lower() == "content-length":
                continue
            headers[key] = value

        if incoming_host:
            headers["Host"] = incoming_host
        headers["X-Forwarded-Host"] = incoming_host or f"{self.server.server_address[0]}:{self.server.server_address[1]}"
        headers["X-Forwarded-Proto"] = self.headers.get("X-Forwarded-Proto", "http")
        headers["X-Forwarded-Prefix"] = upstream.mount_prefix

        body_length = int(self.headers.get("Content-Length", "0") or "0")

        connection = http.client.HTTPConnection(upstream.host, upstream.port, timeout=120)
        try:
            connection.putrequest(self.command, target_path, skip_host=True, skip_accept_encoding=True)
            for key, value in headers.items():
                connection.putheader(key, value)
            if body_length > 0 and self.command not in {"GET", "HEAD"}:
                connection.putheader("Content-Length", str(body_length))
            connection.endheaders()

            if body_length > 0 and self.command not in {"GET", "HEAD"}:
                remaining = body_length
                while remaining > 0:
                    chunk = self.rfile.read(min(65536, remaining))
                    if not chunk:
                        break
                    connection.send(chunk)
                    remaining -= len(chunk)

            upstream_response = connection.getresponse()
            self.send_response(upstream_response.status, upstream_response.reason)

            for key, value in upstream_response.getheaders():
                lower_key = key.lower()
                if lower_key in HOP_BY_HOP_HEADERS:
                    continue
                if lower_key == "location":
                    value = rewrite_location(value, upstream)
                self.send_header(key, value)

            self.end_headers()

            if self.command != "HEAD":
                while True:
                    data = upstream_response.read(65536)
                    if not data:
                        break
                    self.wfile.write(data)
        finally:
            connection.close()

    def do_GET(self) -> None:
        if self._handle_visitor_count():
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
    parser = argparse.ArgumentParser(description="Gateway for LobeChat and Cloud Drive")
    parser.add_argument("--host", default=os.environ.get("GATEWAY_HOST", "127.0.0.1"))
    parser.add_argument("--port", default=int(os.environ.get("GATEWAY_PORT", "8080")), type=int)
    parser.add_argument("--ai-host", default=os.environ.get("GATEWAY_AI_HOST", "127.0.0.1"))
    parser.add_argument("--ai-port", default=int(os.environ.get("GATEWAY_AI_PORT", "3210")), type=int)
    parser.add_argument("--drive-host", default=os.environ.get("GATEWAY_DRIVE_HOST", "127.0.0.1"))
    parser.add_argument("--drive-port", default=int(os.environ.get("GATEWAY_DRIVE_PORT", "8787")), type=int)
    parser.add_argument("--drive-prefix", default=os.environ.get("GATEWAY_DRIVE_PREFIX", "/cloud-drive"))
    args = parser.parse_args()

    # Initialize visitor counter
    counter = VisitorCounter()

    server = ThreadingHTTPServer((args.host, args.port), GatewayHandler)
    server.ai_host = args.ai_host
    server.ai_port = args.ai_port
    server.drive_host = args.drive_host
    server.drive_port = args.drive_port
    server.drive_prefix = normalize_mount_prefix(args.drive_prefix)
    GatewayHandler.visitor_counter = counter

    print(f"Gateway listening on http://{args.host}:{args.port}")
    print(f"AI upstream: http://{server.ai_host}:{server.ai_port}")
    print(f"Cloud Drive upstream: http://{server.drive_host}:{server.drive_port}{server.drive_prefix}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())