# Sihan's Blog | 个人站与云盘入口
> Public-facing entry for files, notes, and source.  
> 面向访客的文件、笔记与源码入口。

![Status](https://img.shields.io/badge/Status-Cloud%20Drive%20Live-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Python-blue)
![Docs](https://img.shields.io/badge/Docs-MkDocs%20%2B%20GitHub%20Pages-8c6f4a)

## 项目定位 | What This Repo Is

这个仓库现在承担两件事：
This repository now serves two public-facing purposes:

- 对外提供一个简洁的个人站入口页，把文件、笔记和代码放在同一个地方。
- It provides a compact personal landing page that groups file access, notes, and source in one place.
- 保存云盘服务、部署文件、文档站源文件，以及和线上状态直接相关的说明。
- It keeps the cloud-drive service code, deployment files, docs source, and notes tied to the live system.

它不是产品宣传页，也不再是功能堆叠的导航页。
It is not a product brochure and no longer tries to be an overloaded dashboard.

## 当前状态 | Current State

以下状态基于 `2026-04-11` 的仓库与服务检查。
The following state reflects repository and service checks from `2026-04-11`.

| Item | Status | Notes |
|---|---|---|
| `cloud-drive.service` | `active` | 公共文件服务在线运行 / Public file service is live |
| `caddy.service` | `active` | 负责 HTTPS 与域名接入 / Handles HTTPS and domain termination |
| `cloud-gateway.service` | `active` | 保留项目网关能力 / Keeps gateway routing available |
| `lobe-chat.service` | `stopped` | 公共 AI 入口已下线 / Public AI entry has been removed |
| GitHub Pages | `200 OK` | `https://sihan-bzwj.github.io/` |
| Cloud drive | `live` | `https://clouddrive.ccwu.cc/` |

## 公共入口 | Public Endpoints

| Service | URL | Description |
|---|---|---|
| Blog / Docs | `https://sihan-bzwj.github.io/` | 个人站首页与公开说明页 / Personal landing page and public notes |
| Cloud Drive | `https://clouddrive.ccwu.cc/` | 文件浏览、上传与下载入口 / File browser, upload, and download entry |
| Source Repo | `https://github.com/sihan-bzwj/sihan-bzwj.github.io` | 源码、配置与文档源文件 / Source code, config, and docs source |

云盘域名指向 Azure VM 公网 IP，并由 Caddy 提供 HTTPS。
The cloud-drive domain points to the Azure VM public IP and is served over HTTPS by Caddy.

## 最近的设计调整 | Recent Site Direction

这个站点最近做过一轮比较彻底的收缩和重写，目标是把它从“说明很多的项目页”调整成“更像个人长期维护的入口页”。
The site recently went through a substantial rewrite to move away from a dense project page and toward a personal, long-lived entry page.

本轮保留的方向：
What stays:

- 首页文案尽量短，只保留真正要给访客看的入口。
- Copy stays short and visitor-facing.
- 视觉上改成偏暗的暖黑色基调，但不用厚重的模糊背景和多余装饰。
- The visual system uses a darker warm-charcoal palette without heavy blur effects or decorative noise.
- 语言从“系统介绍”改成“个人站口吻”，但避免过度抒情。
- The voice shifts from system-description language to a personal-site tone without turning lyrical.

本轮移除的内容：
What was removed:

- 多余的解释卡、状态展示块、平台结构说明区。
- Extra explainer cards, status panels, and architecture showcase sections.
- 为了“看起来复杂”而加入的模糊光斑、视觉占位图和重复标题。
- Blur blobs, decorative placeholders, and repeated headings that only made the page noisier.
- 旧的公共 AI 入口及相关展示。
- The old public AI entry and its related display copy.

## AI 服务下线记录 | AI Removal Record

从 `2026-04-11` 起，仓库和公开文档不再展示公共 AI 入口，服务端的相关公开服务也已经停止。
Starting on `2026-04-11`, the public AI entry was removed from both the repository-facing docs and the running public setup.

原因 | Reasons

- 对外重点已经切换为云盘、笔记和代码入口。
- The public focus is now the drive, notes, and source.
- 旧 AI 入口带来了失效链接和额外维护成本。
- The old AI entry created stale links and unnecessary maintenance overhead.
- 公开文档应只展示真实在线、可持续维护的服务。
- Public docs should only expose services that are actually live and maintainable.

当前处理 | Current Handling

- 公共 AI 入口已移除。
- The public AI entry has been removed.
- `lobe-chat.service` 已停止并禁用。
- `lobe-chat.service` has been stopped and disabled.
- 文档站只保留云盘、说明页和源码仓库入口。
- The docs site now keeps only the drive, notes, and source entry points.

## 架构 | Architecture

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

## 技术栈 | Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| OS | Ubuntu `22.04.5 LTS` | Azure VM 运行环境 / Azure VM runtime |
| Reverse proxy / TLS | Caddy | HTTPS 终止与域名接入 / HTTPS termination and routing |
| Drive service | Python stdlib HTTP service | 文件浏览、上传、下载、删除 / File browsing, upload, download, deletion |
| Gateway | Python `3.10.12` | 项目网关与补充路由 / Project routing and glue logic |
| Docs | MkDocs Material + GitHub Pages | 对外文档与个人站首页 / Public docs and personal landing page |

## 仓库结构 | Repo Structure

| Path | Responsibility |
|---|---|
| `my-project/cloud_drive_app/` | 云盘配置、存储、上传与核心逻辑 / cloud-drive config, storage, uploads, and core logic |
| `my-project/cloud_gateway_app/` | 网关配置、代理、静态内容与路由 / gateway config, proxying, static content, and routing |
| `my-project/cloud_drive_server.py` | 云盘服务入口 / cloud-drive entrypoint |
| `my-project/cloud_gateway.py` | 网关服务入口 / gateway entrypoint |
| `my-project/cloud-drive.service` | 云盘 `systemd` 单元 / `systemd` unit for the drive |
| `my-project/cloud-gateway.service` | 网关 `systemd` 单元 / `systemd` unit for the gateway |
| `my-project/docs/` | GitHub Pages 文档站源文件 / GitHub Pages docs source |
| `my-project/tests/` | 单元测试 / unit tests |

## 文档站模块 | Docs Site Modules

当前文档站的前端已经按职责拆分，尽量避免把样式和行为堆进单个文件。
The docs front end is now split by responsibility instead of piling styles and behavior into one place.

| Path | Responsibility |
|---|---|
| `my-project/mkdocs.yml` | 站点元数据、导航、静态资源注册 / site metadata, nav, and asset registration |
| `my-project/docs/index.md` | 首页内容与入口编排 / homepage content and entry layout |
| `my-project/docs/cloud-drive.md` | 云盘说明页内容 / cloud-drive page content |
| `my-project/docs/stylesheets/fonts.css` | 字体配置 / font setup |
| `my-project/docs/stylesheets/tokens.css` | 颜色、边框、阴影等主题变量 / theme tokens for color, border, and shadow |
| `my-project/docs/stylesheets/base.css` | 全局页面背景与基础覆盖 / global background and base overrides |
| `my-project/docs/stylesheets/components.css` | 导航、按钮、卡片等通用组件 / shared nav, buttons, and cards |
| `my-project/docs/stylesheets/pages.css` | 页面级布局与文案块样式 / page-level layout and content blocks |
| `my-project/docs/javascripts/reveal.js` | 轻量滚动显现脚本 / reveal-on-scroll behavior |
| `my-project/docs/javascripts/theme-toggle.js` | 昼夜主题切换与本地偏好保存 / day-night theme toggle with persisted preference |

## 前端改动说明 | Front-End Notes

这轮前端处理重点不是“做更多”，而是“删掉不必要的部分，再把留下来的部分写稳”。
The front-end work in this round was not about adding more, but about removing noise and stabilizing what remains.

已经落实的处理包括：
Implemented changes include:

- 首页从多段解释结构改成一个简洁主段落加三个入口卡片。
- The homepage was reduced to a compact lead section plus three entry cards.
- 云盘页改成更短的公开说明，不再模拟服务界面。
- The cloud-drive page now uses short public-facing notes instead of imitating the service UI.
- 样式变量统一收口到 `tokens.css`，组件样式集中在 `components.css`，页面布局留在 `pages.css`。
- Theme variables are centralized in `tokens.css`, shared UI in `components.css`, and page layout in `pages.css`.
- 主题切换不只切背景，文字、卡片、按钮、标签和边框都会一起切换。
- Theme switching updates not only the background but also text, cards, buttons, chips, and borders.

## 维护原则 | Maintenance Principles

- 公开页面只展示真实在线、真实可访问的内容。
- Public pages should expose only what is actually live and reachable.
- 文案以访客阅读效率为优先，不把个人维护笔记直接堆到首页。
- Visitor readability comes before dumping maintenance notes into the homepage.
- 代码和样式保持模块化，页面级改动尽量不要污染全局。
- Code and styles stay modular; page-specific changes should not leak into the whole site.
- 注释只写必要的信息，解释职责和边界，不写无意义的废话注释。
- Comments should explain responsibility and boundaries, not narrate obvious syntax.

## 排查命令 | Troubleshooting

```bash
sudo systemctl status cloud-drive.service --no-pager
sudo systemctl status caddy.service --no-pager
sudo systemctl status cloud-gateway.service --no-pager
curl -I https://clouddrive.ccwu.cc/
curl https://clouddrive.ccwu.cc/health
```

## 本地验证 | Local Verification

```bash
python -m mkdocs build -f my-project/mkdocs.yml --strict
cd my-project
python -m unittest discover -s tests
```

## 更新记录 | Update Log

### 2026-04-11

- 恢复并整合旧版 README 里的架构、部署状态、AI 下线记录、关键文件和排查说明。
- Restored and merged architecture, deployment state, AI removal notes, key files, and troubleshooting details from the previous README.
- README 改为中英双语，并调整成面向访客与维护者都能直接阅读的口径。
- Rewrote the README in bilingual language that works for both visitors and maintainers.
- 首页与云盘页重写为更简洁的个人站表达，删除多余说明块和重复视觉结构。
- Rewrote the homepage and cloud-drive page into a simpler personal-site style, removing extra explainer blocks and repeated visual sections.
- 文档站改成更克制的暗色主题，并清理了厚重的模糊背景和装饰性占位图。
- Shifted the docs site to a more restrained dark theme and removed heavy blur backgrounds and decorative placeholders.
- 前端样式继续模块化拆分，并新增 `theme-toggle.js` 处理昼夜主题切换与本地持久化。
- Kept the front-end styles modular and added `theme-toggle.js` for day-night theme switching with local persistence.
