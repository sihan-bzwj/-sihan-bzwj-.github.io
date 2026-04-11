from __future__ import annotations

import http.client
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit

from .routing import HOP_BY_HOP_HEADERS, Upstream, choose_upstream, rewrite_location


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
