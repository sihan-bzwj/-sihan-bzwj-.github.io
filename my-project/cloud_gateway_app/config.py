from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .routing import normalize_mount_prefix


@dataclass(frozen=True)
class GatewayConfig:
    """Runtime configuration for the cloud gateway."""

    host: str
    port: int
    ai_host: str
    ai_port: int
    drive_host: str
    drive_port: int
    drive_prefix: str
    site_dir: Path
    visitor_data_file: Path


def load_gateway_config(
    *,
    host: str | None = None,
    port: int | None = None,
    ai_host: str | None = None,
    ai_port: int | None = None,
    drive_host: str | None = None,
    drive_port: int | None = None,
    drive_prefix: str | None = None,
    site_dir: str | Path | None = None,
    visitor_data_file: str | Path | None = None,
) -> GatewayConfig:
    """Load gateway configuration from CLI arguments and environment variables."""
    return GatewayConfig(
        host=host or os.environ.get("GATEWAY_HOST", "127.0.0.1"),
        port=port if port is not None else int(os.environ.get("GATEWAY_PORT", "8080")),
        ai_host=ai_host or os.environ.get("GATEWAY_AI_HOST", "127.0.0.1"),
        ai_port=ai_port if ai_port is not None else int(os.environ.get("GATEWAY_AI_PORT", "3210")),
        drive_host=drive_host or os.environ.get("GATEWAY_DRIVE_HOST", "127.0.0.1"),
        drive_port=drive_port if drive_port is not None else int(os.environ.get("GATEWAY_DRIVE_PORT", "8787")),
        drive_prefix=normalize_mount_prefix(drive_prefix or os.environ.get("GATEWAY_DRIVE_PREFIX", "/cloud-drive")),
        site_dir=Path(site_dir or os.environ.get("GATEWAY_SITE_DIR", "./site")).resolve(),
        visitor_data_file=Path(visitor_data_file or os.environ.get("GATEWAY_VISITOR_DATA_FILE", ".visitor_ips")).resolve(),
    )
