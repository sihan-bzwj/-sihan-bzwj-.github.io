# my-project
> Service code, deployment files, and the MkDocs source for the public site.

## What Lives Here

- `cloud_drive_app/`: cloud-drive configuration, storage, uploads, and service helpers
- `cloud_gateway_app/`: gateway configuration, routing, proxying, and static-site helpers
- `cloud_drive_server.py`: cloud-drive entrypoint
- `cloud_gateway.py`: gateway entrypoint
- `cloud-drive.service`: `systemd` unit for the drive service
- `cloud-gateway.service`: `systemd` unit for the gateway
- `docs/`: GitHub Pages documentation source
- `tests/`: standard-library unit tests

## Current Deployment Model

```text
Public cloud-drive traffic
  -> clouddrive.ccwu.cc
  -> Azure VM public IP
  -> Caddy (:443)
  -> cloud_drive_server.py on 127.0.0.1:8787

Public docs
  -> GitHub Pages
  -> MkDocs build output generated from docs/
```

## Docs Front-End Layout

The documentation site was reorganized into small, easier-to-maintain front-end modules:

- `docs/index.md`: redesigned homepage
- `docs/cloud-drive.md`: redesigned cloud-drive page
- `docs/stylesheets/fonts.css`: font imports and shared font-family variables
- `docs/stylesheets/tokens.css`: warm palette, spacing, radii, and shadows from `DESIGN.md`
- `docs/stylesheets/base.css`: MkDocs/Material overrides and global defaults
- `docs/stylesheets/components.css`: shared cards, buttons, grids, and reveal states
- `docs/stylesheets/pages.css`: hero illustrations and page-only styling
- `docs/javascripts/reveal.js`: small intersection-observer animation helper

Removed as part of the cleanup:

- Old single-file docs stylesheet
- Visitor-count script and UI dependency
- Legacy iframe preview scaffolding
- Garbled labels in page content and MkDocs metadata

## Principles

- Public docs should show only live, supportable endpoints.
- Static site code should stay modular instead of growing in one CSS file.
- Upload and delete actions remain protected by the server-side password.
- The docs site explains the deployed architecture; it does not emulate the service UI.

## Common Commands

```bash
python cloud_drive_server.py --host 127.0.0.1 --port 8787
python cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s tests
python -m mkdocs build
```

## Update Log

### 2026-04-11

- Rebuilt the docs site around the warm editorial system described in `../DESIGN.md`
- Replaced the previous dark front-end with two focused pages: home and cloud drive
- Split the docs styles into five CSS modules and replaced the old JS with a dedicated reveal module
- Removed visitor-count and iframe-related dead code from the public docs
- Rewrote page copy so it matches the currently deployed cloud-drive service
