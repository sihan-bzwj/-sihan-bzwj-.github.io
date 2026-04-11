# Sihan's Cloud Notes
> Personal cloud-drive services, deployment files, and a redesigned GitHub Pages documentation site.

![Status](https://img.shields.io/badge/Status-Cloud%20Drive%20Live-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Python-blue)
![Docs](https://img.shields.io/badge/Docs-MkDocs%20%2B%20GitHub%20Pages-8c6f4a)

## Current State

The following state reflects the repository and server checks aligned with the current public setup on `2026-04-11`.

| Item | Status | Notes |
|---|---|---|
| `cloud-drive.service` | `active` | Public file service on the Azure VM. |
| `caddy.service` | `active` | Terminates HTTPS for the drive domain. |
| `cloud-gateway.service` | `active` | Available for project routing and related service glue. |
| `lobe-chat.service` | `stopped` | No longer exposed publicly. |
| GitHub Pages | `200 OK` | `https://sihan-bzwj.github.io/` |
| Cloud drive URL | `live` | `https://clouddrive.ccwu.cc/` |

## Public Endpoints

| Service | URL | Description |
|---|---|---|
| Cloud drive | `https://clouddrive.ccwu.cc/` | Public file browser and transfer entry. |
| Docs site | `https://sihan-bzwj.github.io/` | GitHub Pages site for project notes and service guidance. |
| Source repo | `https://github.com/sihan-bzwj/sihan-bzwj.github.io` | Canonical source for docs, service code, and deployment files. |

## Architecture

```text
Public browser
  -> https://clouddrive.ccwu.cc/
    -> DNS A record
    -> Caddy on Azure VM (:443)
    -> cloud_drive_server.py (127.0.0.1:8787)

Public browser
  -> https://sihan-bzwj.github.io/
    -> GitHub Pages
    -> MkDocs static site generated from my-project/docs/
```

## Docs Site Modules

The GitHub Pages site was redesigned around `DESIGN.md` and split into small front-end modules:

| Path | Responsibility |
|---|---|
| `my-project/mkdocs.yml` | Site metadata, page navigation, and asset registration |
| `my-project/docs/index.md` | New editorial-style homepage |
| `my-project/docs/cloud-drive.md` | Cloud-drive service page |
| `my-project/docs/stylesheets/fonts.css` | Purposeful font stacks for serif, sans, and mono text |
| `my-project/docs/stylesheets/tokens.css` | Shared design tokens from `DESIGN.md` |
| `my-project/docs/stylesheets/base.css` | Theme resets and MkDocs/Material overrides |
| `my-project/docs/stylesheets/components.css` | Reusable cards, grids, buttons, and reveal states |
| `my-project/docs/stylesheets/pages.css` | Page-specific hero and illustration treatment |
| `my-project/docs/javascripts/reveal.js` | Lightweight reveal-on-scroll behavior |

Removed from the docs site during this cleanup:

- The previous cold dark theme
- The unused visitor-count fetch logic
- The old iframe-driven cloud-drive preview
- Garbled bilingual labels and broken metadata text
- Redundant homepage sections that no longer matched the live services

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Runtime OS | Ubuntu 22.04.5 LTS | Azure VM host environment |
| Reverse proxy / TLS | Caddy | HTTPS termination and domain routing |
| Drive service | Python stdlib HTTP server | File browsing, upload, download, folder management |
| Gateway | Python 3.10.12 | Routing and static-site support on the VM |
| Docs | MkDocs Material + GitHub Pages | Public documentation site |
| Front-end docs assets | Modular CSS + small vanilla JS | Page layout, styling, and scroll reveal |

## Common Commands

```bash
python my-project/cloud_drive_server.py --host 127.0.0.1 --port 8787
python my-project/cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s my-project/tests
python -m mkdocs build -f my-project/mkdocs.yml
```

```bash
sudo systemctl status cloud-drive.service --no-pager
sudo systemctl status caddy.service --no-pager
curl -I https://clouddrive.ccwu.cc/
curl https://clouddrive.ccwu.cc/health
```

## Update Log

### 2026-04-11

- Rebuilt the GitHub Pages site to match the warm editorial design direction in `DESIGN.md`
- Rewrote the homepage and cloud-drive page with clean bilingual copy and a reduced information hierarchy
- Split docs styling into `fonts.css`, `tokens.css`, `base.css`, `components.css`, and `pages.css`
- Replaced the visitor-count script with a single-purpose `reveal.js` interaction module
- Removed the leftover visitor-count UI, old dark-tech presentation, and iframe preview scaffolding
- Corrected broken site metadata, navigation labels, and other garbled text in the docs source
- Kept the public docs focused on the live cloud-drive and repository entrypoints only
- Preserved the existing Azure VM + Caddy + Python deployment model for the actual file service
