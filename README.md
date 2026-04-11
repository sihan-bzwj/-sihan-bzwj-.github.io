# Sihan's Blog | 思涵的个人网站
> A personal project on an Azure VM, now focused publicly on the cloud drive and documentation site.

![Status](https://img.shields.io/badge/Status-Cloud%20Drive%20Live-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Python-blue)
![HTTPS](https://img.shields.io/badge/HTTPS-Caddy%20%2B%20Let's%20Encrypt-green)

## Current State

The following state is based on the repository and server checks performed on `2026-04-11`.

| Item | Status | Notes |
|---|---|---|
| `cloud-drive.service` | `active` | Cloud drive runs locally on the Azure VM. |
| `caddy.service` | `active` | Terminates HTTPS for the public cloud-drive domain. |
| `cloud-gateway.service` | `active` | Still available on the VM for project routing and docs-related use. |
| `lobe-chat.service` | `stopped` | Public AI access has been removed and the service is offline. |
| GitHub Pages | `200 OK` | `https://sihan-bzwj.github.io/` |
| Cloud drive public URL | `live` | `https://clouddrive.ccwu.cc/` |

## Public Endpoints

| Service | URL | Description |
|---|---|---|
| Cloud drive | `https://clouddrive.ccwu.cc/` | Public cloud-drive entry backed by the Azure VM. |
| Docs site | `https://sihan-bzwj.github.io/` | Public documentation on GitHub Pages. |

The cloud-drive domain now points to the Azure VM public IP and is served over HTTPS by Caddy with Let's Encrypt.

## AI Removal Record

Starting on `2026-04-11`, the repository and public docs no longer expose a public AI entry, and the server-side AI service has been stopped.

Reasons:

- The public project is now centered on the cloud drive and docs, not on keeping an unstable public AI endpoint.
- The old AI entry created stale links and maintenance overhead.
- The drive now has a stable public hostname, so public docs should only keep endpoints that are actually live.

Current handling:

- Public AI entry removed
- `lobe-chat.service` stopped and disabled
- Public docs keep only the cloud-drive and documentation entrypoints

## Architecture

```text
Public browser
  -> https://clouddrive.ccwu.cc/
    -> DNSHE A record
    -> Caddy on Azure VM (:443)
    -> cloud_drive_server.py (127.0.0.1:8787)

Public browser
  -> https://sihan-bzwj.github.io/
    -> GitHub Pages docs
```

## Tech Stack

| Layer | Technology | State / Version | Purpose |
|---|---|---|---|
| OS | Ubuntu | `22.04.5 LTS` | Azure VM runtime environment |
| Reverse proxy / TLS | Caddy | live on server | HTTPS termination and domain routing |
| Drive service | Python stdlib HTTP service | custom | File browsing, upload, download, deletion |
| Gateway | Python 3 | `3.10.12` | Additional project routing on the VM |
| Service manager | systemd | Ubuntu native | Startup, restart, and logs |
| Docs | MkDocs + GitHub Pages | repo-managed | Public docs site |

## Key Repo Files

- `my-project/cloud_drive_server.py`: cloud-drive HTTP server
- `my-project/cloud-drive.service`: `systemd` unit for the drive service
- `my-project/cloud_gateway.py`: project gateway entrypoint
- `my-project/cloud-gateway.service`: `systemd` unit for the gateway
- `my-project/docs/cloud-drive.md`: public docs page for the cloud drive

## Troubleshooting

```bash
sudo systemctl status cloud-drive.service --no-pager
sudo systemctl status caddy.service --no-pager
curl -I https://clouddrive.ccwu.cc/
curl https://clouddrive.ccwu.cc/health
```

## Update Log

### 2026-04-11

- Bound the public cloud-drive domain to `https://clouddrive.ccwu.cc/`
- Terminated HTTPS on the Azure VM with Caddy
- Kept cloud-drive storage on the Azure VM under `/home/azureuser/cloud-drive`
- Removed outdated Render and Quick Tunnel references from the repository
- Added `HEAD` handling to the cloud-drive service so `curl -I /` works
- Refactored the new `HEAD` response path into helper methods and added regression coverage
- Fixed the embedded frontend path-normalization warning caused by escaped regex literals
- Updated the MkDocs cloud-drive page and redeployed GitHub Pages content
- Removed public AI references from the docs site while keeping the record only in README
- Replaced the slow cloud-drive iframe preview with a direct domain link
- Cleaned the garbled MkDocs site title and navigation labels
