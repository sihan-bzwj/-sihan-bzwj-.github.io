from __future__ import annotations

import http.client
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit

from .routing import HOP_BY_HOP_HEADERS, Upstream, choose_upstream, rewrite_location


def build_upstream_unavailable_message(upstream: Upstream, error: Exception | None = None) -> str:
    """Build a clear startup/runtime error message for unavailable upstreams."""
    service_name = "AI platform" if not upstream.mount_prefix else "Cloud Drive"
    message = f"{service_name} upstream is unavailable at http://{upstream.host}:{upstream.port}."
    if error is not None and str(error):
        message = f"{message} Last error: {error}"
    return f"{message} Start the service and retry."


def send_bad_gateway(handler: BaseHTTPRequestHandler, upstream: Upstream, error: Exception) -> None:
    """Return a 502 response instead of dropping the connection on upstream failure."""
    message = build_upstream_unavailable_message(upstream, error)
    if handler.path.startswith("/api/") or upstream.mount_prefix:
        payload = json.dumps({"ok": False, "error": message}).encode("utf-8")
        handler.send_response(502, "Bad Gateway")
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.send_header("Content-Length", str(len(payload)))
        handler.send_header("Cache-Control", "no-store")
        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.end_headers()
        handler.wfile.write(payload)
        return

    payload = message.encode("utf-8")
    handler.send_response(502, "Bad Gateway")
    handler.send_header("Content-Type", "text/plain; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(payload)


def proxy_request(handler: BaseHTTPRequestHandler, ai_upstream: Upstream, drive_upstream: Upstream) -> None:
    """Proxy the current request to the selected upstream service."""
    parsed = urlsplit(handler.path)
    upstream, upstream_path = choose_upstream(parsed.path, ai_upstream, drive_upstream)
    target_path = upstream_path if not parsed.query else f"{upstream_path}?{parsed.query}"

    incoming_host = handler.headers.get("Host")
    headers: dict[str, str] = {}
    for key, value in handler.headers.items():
        if key.lower() in HOP_BY_HOP_HEADERS or key.lower() == "content-length":
            continue
        headers[key] = value

    headers["Host"] = incoming_host or f"{upstream.host}:{upstream.port}"
    headers["X-Forwarded-Host"] = incoming_host or f"{handler.server.server_address[0]}:{handler.server.server_address[1]}"
    headers["X-Forwarded-Proto"] = handler.headers.get("X-Forwarded-Proto", "http")
    headers["X-Forwarded-Prefix"] = upstream.mount_prefix

    body_length = int(handler.headers.get("Content-Length", "0") or "0")
    connection = http.client.HTTPConnection(upstream.host, upstream.port, timeout=120)
    try:
        try:
            connection.putrequest(handler.command, target_path, skip_host=True, skip_accept_encoding=True)
            for key, value in headers.items():
                connection.putheader(key, value)
            if body_length > 0 and handler.command not in {"GET", "HEAD"}:
                connection.putheader("Content-Length", str(body_length))
            connection.endheaders()

            if body_length > 0 and handler.command not in {"GET", "HEAD"}:
                remaining = body_length
                while remaining > 0:
                    chunk = handler.rfile.read(min(65536, remaining))
                    if not chunk:
                        break
                    connection.send(chunk)
                    remaining -= len(chunk)

            upstream_response = connection.getresponse()
        except (OSError, http.client.HTTPException) as error:
            send_bad_gateway(handler, upstream, error)
            return

        handler.send_response(upstream_response.status, upstream_response.reason)
        for key, value in upstream_response.getheaders():
            lower_key = key.lower()
            if lower_key in HOP_BY_HOP_HEADERS:
                continue
            if lower_key == "location":
                value = rewrite_location(value, upstream)
            handler.send_header(key, value)
        handler.end_headers()

        if handler.command != "HEAD":
            while True:
                data = upstream_response.read(65536)
                if not data:
                    break
                handler.wfile.write(data)
    finally:
        connection.close()
