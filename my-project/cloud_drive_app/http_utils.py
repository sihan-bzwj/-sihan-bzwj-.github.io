from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


def request_json(handler: BaseHTTPRequestHandler) -> dict[str, object]:
    """Read and decode a JSON request body."""
    content_length = int(handler.headers.get("Content-Length", "0") or "0")
    if content_length <= 0:
        return {}
    raw_body = handler.rfile.read(content_length)
    if not raw_body:
        return {}
    return json.loads(raw_body.decode("utf-8"))


def write_response(handler: BaseHTTPRequestHandler, status: HTTPStatus, content_type: str, data: bytes) -> None:
    """Send a standard response with the shared API headers."""
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, X-Upload-Password")
    handler.end_headers()
    handler.wfile.write(data)


def send_json(handler: BaseHTTPRequestHandler, status: HTTPStatus, payload: dict[str, object]) -> None:
    """Send a UTF-8 JSON response."""
    write_response(
        handler,
        status,
        "application/json; charset=utf-8",
        json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    )


def send_text(
    handler: BaseHTTPRequestHandler,
    status: HTTPStatus,
    content: str,
    content_type: str = "text/plain; charset=utf-8",
) -> None:
    """Send a plain-text response."""
    write_response(handler, status, content_type, content.encode("utf-8"))


def send_html(handler: BaseHTTPRequestHandler, status: HTTPStatus, content: str) -> None:
    """Send an HTML response."""
    write_response(handler, status, "text/html; charset=utf-8", content.encode("utf-8"))


def parse_query(path: str) -> tuple[str, dict[str, list[str]]]:
    """Split a request path into path and query-string values."""
    parsed = urlparse(path)
    return parsed.path, parse_qs(parsed.query)


def get_query_value(values: dict[str, list[str]], key: str, default: str = "") -> str:
    """Read the first query-string value for a given key."""
    value_list = values.get(key)
    if not value_list:
        return default
    return value_list[0]
