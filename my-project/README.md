# my-project | 实现与部署说明
> This directory contains the service code, deployment files, and documentation source.

## What Lives Here

- `cloud_drive_app/`: config, path handling, upload parsing, and business logic for the drive service
- `cloud_gateway_app/`: gateway config, reverse proxying, static-site serving, and visitor counting
- `cloud_drive_server.py`: cloud-drive entrypoint
- `cloud_gateway.py`: gateway entrypoint
- `cloud-drive.service`: `systemd` unit for the drive service
- `cloud-gateway.service`: `systemd` unit for the gateway
- `docs/`: MkDocs documentation source
- `tests/`: standard-library unit tests

## Current Deployment Model

```text
Public cloud-drive traffic
  -> clouddrive.ccwu.cc
  -> Azure VM public IP
  -> Caddy (:80)
  -> cloud_drive_server.py on 127.0.0.1:8787

Public docs
  -> GitHub Pages
```

Key points:

- The public cloud-drive domain terminates on Caddy, not on Render.
- Uploaded files remain on the Azure VM.
- The AI service is no longer part of the public deployment.

## Server-Verified State

Based on the actual server checks performed on `2026-04-11`:

- `cloud-drive.service`: `active`
- `caddy.service`: `active`
- `cloud-gateway.service`: `active`
- `lobe-chat.service`: `stopped`
- `http://clouddrive.ccwu.cc/health`: live

## Principles

- Public docs should only show URLs that are already live.
- Cloud-drive storage stays on the Azure VM.
- Caddy currently serves the drive over HTTP because Azure inbound `443` is still blocked externally.
- Repo docs should match the deployed architecture.

## Tech Stack

| Component | Technology | Notes |
|---|---|---|
| Drive service | Python stdlib HTTP server | Directory browsing, upload, download, deletion |
| Reverse proxy | Caddy | Public HTTP for `clouddrive.ccwu.cc` |
| Gateway | Python stdlib HTTP server | Project routing and static content support |
| Docs | MkDocs + GitHub Pages | Docs site and landing pages |
| Service manager | systemd | Keeps services ordered and running |

## Common Commands

```bash
python cloud_drive_server.py --host 127.0.0.1 --port 8787
python cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s tests
```

```bash
sudo systemctl status cloud-drive.service --no-pager
sudo systemctl status caddy.service --no-pager
sudo systemctl status cloud-gateway.service --no-pager
curl -I http://clouddrive.ccwu.cc/
curl http://clouddrive.ccwu.cc/health
```

## Update Log

### 2026-04-11

- Switched the public cloud-drive entry to `http://clouddrive.ccwu.cc/`
- Switched Caddy to temporary HTTP-only serving because Azure inbound `443` is still blocked externally
- Kept file storage on the Azure VM instead of moving it to a hosted platform
- Removed outdated deployment artifacts and placeholder-domain references
- Added `HEAD` support to the cloud-drive HTTP service
- Refactored `HEAD` handling into small helper methods with targeted comments
- Added a regression test for `HEAD /`
- Re-published the docs site so the cloud-drive page no longer points at `drive.example.com`
- Removed public AI mentions from the docs site pages
- Replaced the embedded cloud-drive iframe with a direct access section
- Cleaned `mkdocs.yml` site metadata and navigation labels
