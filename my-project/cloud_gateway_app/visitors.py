from __future__ import annotations

import threading
from pathlib import Path


class IPVisitorCounter:
    """Thread-safe IP visitor counter with file persistence."""

    def __init__(self, file_path: str | Path = ".visitor_ips"):
        self.file_path = Path(file_path)
        self.lock = threading.Lock()
        self.visitor_ips: set[str] = set()
        self._load()

    def _load(self) -> None:
        if not self.file_path.exists():
            self.visitor_ips = set()
            return

        try:
            content = self.file_path.read_text(encoding="utf-8").strip()
            self.visitor_ips = {ip.strip() for ip in content.splitlines() if ip.strip()}
        except (OSError, ValueError):
            self.visitor_ips = set()

    def _save(self) -> None:
        try:
            self.file_path.write_text("\n".join(sorted(self.visitor_ips)), encoding="utf-8")
        except OSError:
            pass

    def record_visitor(self, ip: str) -> int:
        """Record an IP and return the total number of unique visitors."""
        cleaned_ip = ip.split(":", 1)[0].strip()
        with self.lock:
            self.visitor_ips.add(cleaned_ip)
            self._save()
            return len(self.visitor_ips)

    def get_count(self) -> int:
        """Return the number of unique visitors seen so far."""
        with self.lock:
            return len(self.visitor_ips)
