from __future__ import annotations

import shutil
from pathlib import Path

from .storage import (
    file_metadata,
    list_directory,
    make_unique_path,
    parent_relative_path,
    relative_path,
    resolve_inside_root,
    safe_name,
    storage_usage,
)
from .uploads import UploadedFile


def health_payload(root: Path) -> dict[str, object]:
    """Build the lightweight health response for monitoring."""
    return {"ok": True, "storage": storage_usage(root)}


def list_directory_payload(root: Path, requested_path: str) -> dict[str, object]:
    """Build the response payload for directory browsing."""
    folder = resolve_inside_root(root, requested_path)
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError("目录不存在")

    current_path = relative_path(folder.relative_to(root).as_posix())
    return {
        "ok": True,
        "path": current_path,
        "parent": parent_relative_path(current_path),
        "entries": list_directory(root, folder),
        "storage": storage_usage(root),
    }


def download_path(root: Path, requested_path: str) -> Path:
    """Resolve and validate a downloadable file path."""
    file_path = resolve_inside_root(root, requested_path)
    if not file_path.is_file():
        raise FileNotFoundError("文件不存在")
    return file_path


def store_uploads(root: Path, requested_path: str, files: list[UploadedFile]) -> list[dict[str, object]]:
    """Write uploaded files into the target directory."""
    folder = resolve_inside_root(root, requested_path)
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError("目标目录不存在")

    uploaded: list[dict[str, object]] = []
    for field in files:
        filename = safe_name(field.filename or "")
        destination = make_unique_path(folder / filename)
        with destination.open("wb") as destination_handle:
            shutil.copyfileobj(field.file, destination_handle, length=1024 * 1024)
        uploaded.append(file_metadata(root, destination))

    return uploaded


def create_directory(root: Path, requested_path: str, name: str) -> dict[str, object]:
    """Create a new directory inside the storage root."""
    folder = resolve_inside_root(root, requested_path)
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError("目标目录不存在")

    new_folder = folder / safe_name(name)
    new_folder.mkdir(parents=True, exist_ok=False)
    return file_metadata(root, new_folder)


def delete_entry(root: Path, requested_path: str) -> None:
    """Delete a file or directory while protecting the storage root itself."""
    target = resolve_inside_root(root, requested_path)
    if target == root:
        raise ValueError("不允许删除根目录")

    if target.is_dir():
        shutil.rmtree(target)
        return
    if target.exists():
        target.unlink()
        return
    raise FileNotFoundError("目标不存在")
