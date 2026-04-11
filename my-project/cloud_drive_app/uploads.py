from __future__ import annotations

from dataclasses import dataclass
from email.parser import BytesParser
from email.policy import default as default_email_policy
from http.server import BaseHTTPRequestHandler
from io import BytesIO


@dataclass
class UploadedFile:
    """A parsed multipart file upload."""

    filename: str
    file: BytesIO


def parse_uploaded_files(handler: BaseHTTPRequestHandler) -> list[UploadedFile]:
    """Parse multipart/form-data uploads into in-memory file objects."""
    content_length = int(handler.headers.get("Content-Length", "0") or "0")
    if content_length <= 0:
        return []

    content_type = handler.headers.get("Content-Type", "")
    if not content_type.startswith("multipart/form-data"):
        raise ValueError("上传接口只接受 multipart/form-data")

    raw_body = handler.rfile.read(content_length)
    if not raw_body:
        return []

    parser = BytesParser(policy=default_email_policy)
    message = parser.parsebytes(
        f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8") + raw_body
    )

    uploaded_files: list[UploadedFile] = []
    if not message.is_multipart():
        return uploaded_files

    for part in message.iter_parts():
        if part.get_content_disposition() != "form-data":
            continue
        if part.get_param("name", header="content-disposition") != "file":
            continue

        filename = part.get_filename()
        if not filename:
            continue

        payload = part.get_payload(decode=True) or b""
        uploaded_files.append(UploadedFile(filename=filename, file=BytesIO(payload)))

    return uploaded_files
