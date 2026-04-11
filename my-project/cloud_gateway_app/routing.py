from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True)
class Upstream:
    """One proxied upstream target."""

    host: str
    port: int
    mount_prefix: str = ""


def normalize_mount_prefix(value: str) -> str:
    """Normalize mount prefixes so routing logic can rely on one format."""
    cleaned = "/" + value.strip("/")
    return "" if cleaned == "/" else cleaned


def choose_upstream(path: str, ai_upstream: Upstream, drive_upstream: Upstream) -> tuple[Upstream, str]:
    """Route cloud-drive requests to the drive upstream and everything else to AI."""
    prefix = drive_upstream.mount_prefix
    if prefix and (path == prefix or path.startswith(prefix + "/")):
        stripped_path = path[len(prefix):] or "/"
        return drive_upstream, stripped_path
    return ai_upstream, path


def rewrite_location(location: str, upstream: Upstream) -> str:
    """Rewrite upstream redirects so mounted services stay under their public prefix."""
    prefix = upstream.mount_prefix
    if not prefix:
        return location

    parsed = urlsplit(location)
    if parsed.scheme and parsed.netloc:
        if parsed.hostname in {upstream.host, "localhost", "127.0.0.1"} and parsed.port in {None, upstream.port}:
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
