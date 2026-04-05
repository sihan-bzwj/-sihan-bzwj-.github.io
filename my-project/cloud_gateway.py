#!/usr/bin/env python3

from __future__ import annotations

import argparse
import http.client
import json
import mimetypes
import os
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote, urlunsplit


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


class IPVisitorCounter:
    """Thread-safe IP-based visitor counter with deduplication.
    
    Tracks unique visitor IPs and stores them persistently.
    """
    def __init__(self, file_path: str = ".visitor_ips"):
        self.file_path = Path(file_path)
        self.lock = threading.Lock()
        self.visitor_ips: set[str] = set()
        self._load()

    def _load(self) -> None:
        """Load existing visitor IPs from file."""
        if self.file_path.exists():
            try:
                content = self.file_path.read_text().strip()
                if content:
                    self.visitor_ips = set(ip.strip() for ip in content.split('\n') if ip.strip())
                else:
                    self.visitor_ips = set()
            except (ValueError, OSError):
                self.visitor_ips = set()
        else:
            self.visitor_ips = set()

    def _save(self) -> None:
        """Persist visitor IPs to file."""
        try:
            content = '\n'.join(sorted(self.visitor_ips))
            self.file_path.write_text(content)
        except OSError:
            pass

    def record_visitor(self, ip: str) -> int:
        """Record a visitor IP and return total unique visitor count."""
        # Extract IP without port
        ip = ip.split(':')[0].strip()
        
        with self.lock:
            self.visitor_ips.add(ip)
            self._save()
            return len(self.visitor_ips)

    def get_count(self) -> int:
        """Get total unique visitor count."""
        with self.lock:
            return len(self.visitor_ips)


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
    visitor_counter: IPVisitorCounter | None = None
    site_directory: Path | None = None

    def _get_client_ip(self) -> str:
        """Extract real client IP, handling Cloudflare headers."""
        # Check for Cloudflare header first
        if "CF-Connecting-IP" in self.headers:
            return self.headers["CF-Connecting-IP"]
        
        # Fall back to X-Forwarded-For
        if "X-Forwarded-For" in self.headers:
            return self.headers["X-Forwarded-For"].split(",")[0].strip()
        
        # Use direct connection IP
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
                # Record the visitor's IP
                client_ip = self._get_client_ip()
                count = self.visitor_counter.record_visitor(client_ip)
                self._send_json_response(200, {"count": count, "success": True})
                return True
            elif self.command == "OPTIONS":
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()
                return True
        return False

    def _serve_static_file(self) -> bool:
        """Serve static files from site/ directory. Return True if served."""
        if self.site_directory is None or not self.site_directory.exists():
            return False
        
        # Parse the requested path
        parsed = urlsplit(self.path)
        file_path = unquote(parsed.path)
        
        # Prevent directory traversal attacks
        if ".." in file_path or file_path.startswith("/."):
            return False
        
        # Map root to index.html
        if file_path == "/" or file_path == "":
            file_path = "/index.html"
        
        # Try to find the file
        full_path = (self.site_directory / file_path.lstrip("/")).resolve()
        
        # Security: ensure the resolved path is still within site_directory
        try:
            full_path.relative_to(self.site_directory)
        except ValueError:
            return False
        
        # Check if file exists
        if not full_path.exists():
            # Try index.html for directories
            if full_path.is_dir():
                index_path = full_path / "index.html"
                if index_path.exists():
                    full_path = index_path
                else:
                    return False
            else:
                return False
        
        if not full_path.is_file():
            return False
        
        # Serve the file
        try:
            mime_type, _ = mimetypes.guess_type(str(full_path))
            if mime_type is None:
                mime_type = "application/octet-stream"
            
            with open(full_path, "rb") as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            
            # Cache static assets but not HTML
            if mime_type not in {"text/html", "application/json"}:
                self.send_header("Cache-Control", "public, max-age=3600")
            else:
                self.send_header("Cache-Control", "no-cache, must-revalidate")
            
            self.end_headers()
            self.wfile.write(content)
            return True
        except (IOError, OSError):
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
        # Priority: API > Cloud Drive > Static files > AI proxy
        if self._handle_visitor_count():
            return
        
        parsed = urlsplit(self.path)
        drive_prefix = self.server.drive_prefix
        
        # Check if it's a cloud drive request
        if drive_prefix and (parsed.path == drive_prefix or parsed.path.startswith(drive_prefix + "/")):
            self._proxy()
            return
        
        # Try to serve static files (for website)
        if self._serve_static_file():
            return
        
        # Fall back to AI proxy (LobeChat)
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
    parser.add_argument("--host", default=os.environ.get("GATEWAY_HOST", "127.0.0.1"))
    parser.add_argument("--port", default=int(os.environ.get("GATEWAY_PORT", "8080")), type=int)
    parser.add_argument("--ai-host", default=os.environ.get("GATEWAY_AI_HOST", "127.0.0.1"))
    parser.add_argument("--ai-port", default=int(os.environ.get("GATEWAY_AI_PORT", "3210")), type=int)
    parser.add_argument("--drive-host", default=os.environ.get("GATEWAY_DRIVE_HOST", "127.0.0.1"))
    parser.add_argument("--drive-port", default=int(os.environ.get("GATEWAY_DRIVE_PORT", "8787")), type=int)
    parser.add_argument("--drive-prefix", default=os.environ.get("GATEWAY_DRIVE_PREFIX", "/cloud-drive"))
    parser.add_argument("--site-dir", default=os.environ.get("GATEWAY_SITE_DIR", "./site"))
    args = parser.parse_args()

    # Initialize visitor counter
    counter = IPVisitorCounter()
    
    # Set up site directory
    site_dir = Path(args.site_dir).resolve()

    server = ThreadingHTTPServer((args.host, args.port), GatewayHandler)
    server.ai_host = args.ai_host
    server.ai_port = args.ai_port
    server.drive_host = args.drive_host
    server.drive_port = args.drive_port
    server.drive_prefix = normalize_mount_prefix(args.drive_prefix)
    GatewayHandler.visitor_counter = counter
    GatewayHandler.site_directory = site_dir

    print(f"Gateway listening on http://{args.host}:{args.port}")
    print(f"AI upstream: http://{server.ai_host}:{server.ai_port}")
    print(f"Cloud Drive upstream: http://{server.drive_host}:{server.drive_port}{server.drive_prefix}")
    print(f"Static site directory: {site_dir}")
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
