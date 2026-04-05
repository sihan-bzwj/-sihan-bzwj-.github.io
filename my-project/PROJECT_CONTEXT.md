# Project Context

## One-Sentence Summary
This repository is a MkDocs-based landing site that routes users to two things: LobeChat for conversation and a remote-server-backed cloud drive for file storage.

## Site Idea
- The site is intentionally simple: one strong homepage and one dedicated cloud-drive page.
- The homepage works as the main entry point and should make the two primary actions obvious immediately.
- The cloud drive is not a mock or static download page; it is a real remote backend exposed through a tunnel.
- The visual style is meant to feel like a polished product landing page, not a generic documentation index.

## Information Architecture
- [docs/index.md](docs/index.md) is the homepage and should stay focused on fast navigation.
- [docs/cloud-drive.md](docs/cloud-drive.md) is the cloud-drive landing page and also embeds the actual remote file manager.
- [mkdocs.yml](mkdocs.yml) controls the navigation order and should keep the site structure minimal.

## Current UX Pattern
- The homepage presents two primary CTAs: open LobeChat and open the cloud drive.
- Below the main "内容入口" section, there is an "应用入口" section that displays cards describing each service:
  - **AI 站点**: Introduces LobeChat with its features (multi-model support, customization, fast switching)
  - **Cloud Drive**: Describes the remote storage service (file upload/download, cloud backend, password-protected uploads)
- Each service card includes a brief description, tags, and action buttons for direct access.
- The cloud-drive page explains how the storage works, then embeds the live interface below the explanation.
- Both pages use bold backgrounds, cards, and large spacing so the user immediately understands the site as a remote-access hub.
- The cloud-drive link should remain visible without scrolling, both in the hero actions and in the top navigation.

## Current Visual System
- The default MkDocs top navbar is hidden so the custom in-page header becomes the visible site chrome.
- The visible site header is the `site-shell` block in [docs/index.md](docs/index.md) and [docs/cloud-drive.md](docs/cloud-drive.md), which carries the brand, AI link, GitHub link, and the main page actions.
- The left MkDocs sidebar/TOC column is hidden to remove empty template chrome and keep the page focused on the custom layout.
- The shared styling lives in [docs/stylesheets/extra.css](docs/stylesheets/extra.css) and should be updated whenever the homepage or cloud-drive spacing, colors, or header treatment changes.
- **Application cards styling**: The "应用入口" section uses `.cards` grid container with `.card` + `.info-panel` classes for LobeChat and Cloud Drive service descriptions. Each card has:
  - `.card-header` with a `.kicker` tag and `<h3>` title
  - A description paragraph with `.info-panel` styles
  - `.tag-list` for feature tags
  - `.card-actions` with `margin-top: auto` to pin action buttons to the card bottom

## Backend / Deployment Model
- The cloud drive runs on a remote Azure VM and stores files there instead of locally in the browser.
- The backend listens on `127.0.0.1:8787` on the VM and is exposed through a Cloudflare tunnel.
- Uploads require a password and are checked server-side with the `X-Upload-Password` header.
- Downloads remain public.
- Files are stored under `/home/azureuser/cloud-drive` on the VM.

## Implementation Decisions
- Keep the site MkDocs-based so visible changes stay in `docs/` and can be regenerated with `mkdocs build`.
- Keep the homepage concise and action-oriented rather than turning it into a long explanation page.
- Keep the cloud-drive page visually distinct so users can tell it is a live service entry, not just documentation.
- Use the embedded frame as the primary interaction surface, with a separate open button as a fallback.
- If the tunnel URL changes, update the cloud-drive links in both [docs/cloud-drive.md](docs/cloud-drive.md) and [docs/index.md](docs/index.md).
- If the site chrome changes, update [docs/stylesheets/extra.css](docs/stylesheets/extra.css) first, then rebuild so the generated site stays in sync.

## Files To Check First Next Time
- [docs/index.md](docs/index.md)
- [docs/cloud-drive.md](docs/cloud-drive.md)
- [cloud_drive_server.py](cloud_drive_server.py)
- [deploy-cloud-drive.sh](deploy-cloud-drive.sh)
- [mkdocs.yml](mkdocs.yml)

## Verification Notes
- `mkdocs build` completed successfully after the site changes.
