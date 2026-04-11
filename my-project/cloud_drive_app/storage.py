from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path


def human_size(byte_count: int) -> str:
    """Format raw byte counts into a compact human-readable string."""
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(byte_count)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{byte_count} B"


def iso_timestamp(timestamp: float) -> str:
    """Convert POSIX timestamps into local ISO 8601 strings."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone().isoformat(timespec="seconds")


def relative_path(value: str) -> str:
    """Normalize incoming paths into safe project-relative POSIX paths."""
    normalized = value.strip().lstrip("/")
    if not normalized or normalized == ".":
        return ""
    return Path(normalized).as_posix()


def resolve_inside_root(root: Path, relative_value: str) -> Path:
    """Resolve a relative path and reject traversal outside the storage root."""
    candidate = (root / relative_path(relative_value)).resolve()
    if candidate == root or root in candidate.parents:
        return candidate
    raise ValueError("Path escapes storage root")


def safe_name(value: str) -> str:
    """Return a single safe filename component."""
    candidate = Path(value).name.strip()
    if not candidate or candidate in {".", ".."}:
        raise ValueError("Invalid name")
    return candidate


def parent_relative_path(value: str) -> str:
    """Return the normalized parent path for breadcrumb navigation."""
    cleaned = relative_path(value)
    if not cleaned:
        return ""
    parent = Path(cleaned).parent.as_posix()
    return "" if parent == "." else parent


def make_unique_path(base_path: Path) -> Path:
    """Avoid filename collisions by appending a numbered suffix."""
    if not base_path.exists():
        return base_path

    suffix = "".join(base_path.suffixes)
    stem = base_path.name[: -len(suffix)] if suffix else base_path.name

    for index in range(1, 10_000):
        candidate_name = f"{stem} ({index}){suffix}"
        candidate_path = base_path.with_name(candidate_name)
        if not candidate_path.exists():
            return candidate_path

    raise RuntimeError("Cannot allocate a unique filename")


def file_metadata(root: Path, file_path: Path) -> dict[str, object]:
    """Build the JSON payload used by the frontend file browser."""
    stat_result = file_path.stat()
    kind = "directory" if file_path.is_dir() else "file"
    return {
        "name": file_path.name,
        "path": relative_path(file_path.relative_to(root).as_posix()),
        "kind": kind,
        "size": stat_result.st_size if file_path.is_file() else 0,
        "modified": iso_timestamp(stat_result.st_mtime),
    }


def list_directory(root: Path, folder_path: Path) -> list[dict[str, object]]:
    """List visible children in directories-first order."""
    entries: list[dict[str, object]] = []
    for child in sorted(folder_path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        if child.is_symlink():
            continue
        entries.append(file_metadata(root, child))
    return entries


def storage_usage(root: Path) -> dict[str, object]:
    """Expose disk usage metrics for UI cards and health checks."""
    usage = shutil.disk_usage(root)
    return {
        "root": str(root),
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
    }
