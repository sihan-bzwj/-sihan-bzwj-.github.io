from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_STORAGE_ROOT = "/home/azureuser/cloud-drive"
DEFAULT_UPLOAD_PASSWORD = "sihan123"


def build_root(path_value: str | None) -> Path:
    """Resolve and create the cloud drive root directory."""
    root_path = Path(path_value or os.environ.get("CLOUD_DRIVE_ROOT", DEFAULT_STORAGE_ROOT)).expanduser()
    root_path.mkdir(parents=True, exist_ok=True)
    return root_path.resolve()


@dataclass(frozen=True)
class CloudDriveConfig:
    """Runtime configuration for the cloud drive HTTP service."""

    root: Path
    upload_password: str


def load_config(
    root_override: str | None = None,
    upload_password_override: str | None = None,
) -> CloudDriveConfig:
    """Load cloud drive configuration from CLI arguments and environment variables."""
    return CloudDriveConfig(
        root=build_root(root_override),
        upload_password=upload_password_override
        or os.environ.get("CLOUD_DRIVE_UPLOAD_PASSWORD", DEFAULT_UPLOAD_PASSWORD),
    )
