from __future__ import annotations

import mimetypes
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit


def serve_static_file(handler: BaseHTTPRequestHandler, site_directory: Path | None, request_path: str) -> bool:
    """Serve files from the built MkDocs directory when they exist locally."""
    if site_directory is None or not site_directory.exists():
        return False

    parsed = urlsplit(request_path)
    file_path = unquote(parsed.path)

    if ".." in file_path or file_path.startswith("/."):
        return False

    if file_path in {"/", ""}:
        file_path = "/index.html"

    full_path = (site_directory / file_path.lstrip("/")).resolve()
    try:
        full_path.relative_to(site_directory)
    except ValueError:
        return False

    if not full_path.exists():
        if full_path.is_dir():
            index_path = full_path / "index.html"
            if not index_path.exists():
                return False
            full_path = index_path
        else:
            return False

    if not full_path.is_file():
        return False

    try:
        mime_type, _ = mimetypes.guess_type(str(full_path))
        if mime_type is None:
            mime_type = "application/octet-stream"

        with open(full_path, "rb") as file_handle:
            content = file_handle.read()

        handler.send_response(200)
        handler.send_header("Content-Type", mime_type)
        handler.send_header("Content-Length", str(len(content)))
        if mime_type not in {"text/html", "application/json"}:
            handler.send_header("Cache-Control", "public, max-age=3600")
        else:
            handler.send_header("Cache-Control", "no-cache, must-revalidate")
        handler.end_headers()
        handler.wfile.write(content)
        return True
    except (OSError, IOError):
        return False
