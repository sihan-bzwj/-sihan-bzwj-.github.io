# Project Context

## Current Goal
Build a simple documentation site that acts as a landing page for LobeChat and a remote-server-backed cloud drive.

## What Was Implemented
- Home page updated to be a stronger entry screen with clear CTAs for LobeChat and the cloud drive.
- Cloud drive page added at docs/cloud-drive.md.
- Python cloud drive backend added in cloud_drive_server.py.
- systemd units added for the cloud drive API and the Cloudflare tunnel.
- Deployment script added in deploy-cloud-drive.sh.
- MkDocs navigation now includes the cloud drive page.

## Remote Deployment Notes
- Remote VM: 20.196.193.8
- Cloud drive service listens on 127.0.0.1:8787
- Cloudflare tunnel was used to expose the cloud drive publicly.
- Current cloud drive URL at the time of implementation: https://always-secrets-browsers-flights.trycloudflare.com

## Design / Implementation Decisions
- The cloud drive is a separate remote backend, not just a static download page.
- The site stays MkDocs-based, so all visible changes should be made in docs/ and rebuilt with mkdocs build.
- The cloud drive page uses a large embedded frame and bold landing-page styling to make the frontend change obvious.
- The backend stores files under /home/azureuser/cloud-drive on the VM.
- The homepage should keep a direct cloud-drive entry in the hero actions area so the link is visible without scrolling.

## Files To Check First Next Time
- docs/index.md
- docs/cloud-drive.md
- cloud_drive_server.py
- deploy-cloud-drive.sh
- mkdocs.yml

## Verification
- mkdocs build completed successfully after the changes.
