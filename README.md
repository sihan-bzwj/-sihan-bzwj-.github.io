# Sihan's Blog | 思涵的个人网站

> 一个基于 Azure VM、Docker、Cloudflare Tunnel 和 MkDocs 的个人站点，同时承载云盘与 AI 对话入口。
> A personal website built on Azure VM, Docker, Cloudflare Tunnel, and MkDocs, with cloud drive and AI chat entrypoints.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick-orange)

---

## 项目概览 | Overview

这是一个面向展示、日常使用和长期维护的个人网站与双服务平台，把 AI 对话和个人云盘放在同一套基础设施里统一管理。
This repository combines the personal website, AI chat, and personal cloud storage on one infrastructure stack for demos, daily use, and long-term maintenance.

项目的目标不是只跑通一个网页，而是把前端、后端、隧道、静态文档和系统服务一起组织起来，形成一套可以持续维护的完整方案。
The goal is not just to run a web page, but to keep the frontend, backend, tunnel, static docs, and system services organized as a maintainable end-to-end setup.

### 你会得到什么 | What You Get

- 一个可以公开访问的 AI 对话入口。
- A public AI chat entrypoint.
- 一个可浏览、可上传、可管理的个人云盘。
- A cloud drive that supports browsing, uploads, and file management.
- 一套能够长期维护的部署和文档结构。
- A deployment and documentation structure that can be maintained over time.

### 适用场景 | Typical Uses

- 演示环境和作品集展示。
- Demo environments and portfolio showcases.
- 个人知识整理与文件托管。
- Personal knowledge organization and file hosting.
- 日常访问的轻量云端工具集合。
- A lightweight set of cloud tools for daily use.
- 需要统一管理多个模型供应商的 AI 聊天场景。
- AI chat scenarios that need unified management of multiple model providers.

---

## 在线入口 | Live Access

| 服务 | 地址 | 说明 |
|------|------|------|
| AI 对话平台 | https://procurement-trying-beside-beginning.trycloudflare.com | LobeChat 主界面 / Main interface |
| 云盘 | https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive | 文件管理 / File management |
| 项目主页 | https://sihan-bzwj.github.io/-sihan-bzwj-.github.io/ | 介绍页面 / Landing page |
| 仓库地址 | https://github.com/sihan-bzwj/-sihan-bzwj-.github.io | 源码与文档 / Source and docs |

> Cloudflare Quick Tunnel 的公开地址可能会随着重新创建隧道而变化，访问前请以最新配置为准。
> The public Cloudflare Quick Tunnel URL may change when the tunnel is recreated, so use the latest configured address.

---

## 功能细节 | Feature Details

### AI 对话平台 | AI Chat Platform

- LobeChat 多模型对话界面，基于 Next.js + Node.js。
- Multi-model LobeChat interface built with Next.js + Node.js.
- 支持多个主流模型源，包括 OpenRouter、OpenAI、Anthropic、DeepSeek 等。
- Supports multiple mainstream model providers, including OpenRouter, OpenAI, Anthropic, and DeepSeek.
- 模型列表可以动态获取，减少手工维护成本。
- Model lists can be fetched dynamically to reduce manual maintenance.
- API 密钥由后端代理处理，避免前端直接暴露敏感信息。
- API keys are proxied by the backend so sensitive values are not exposed in the frontend.
- 适合把不同供应商统一到同一个聊天入口中。
- Designed to unify multiple providers behind one chat experience.

### 个人云盘 | Cloud Drive

- 支持上传、下载、删除、重命名和目录管理。
- Supports upload, download, delete, rename, and directory management.
- 支持目录树展示，便于浏览文件结构。
- Provides a tree view for easier navigation of the file hierarchy.
- 支持密码保护上传，适合公网访问场景。
- Supports password-protected uploads for public-access scenarios.
- 提供简洁的 Web 前端，适合手机和桌面浏览器。
- Provides a clean web frontend that works well on mobile and desktop browsers.

### 运维特性 | Operational Features

- 24/7 公网访问，基于 Cloudflare 隧道。
- 24/7 public access powered by Cloudflare Tunnel.
- Docker 负责应用隔离和基础部署。
- Docker provides application isolation and deployment portability.
- systemd 负责守护进程管理和自动重启。
- systemd handles service supervision and automatic restart.
- GitHub Pages + MkDocs 作为项目介绍页。
- GitHub Pages + MkDocs serve as the project landing page.

---

## 系统架构 | Architecture

```text
Browser / Web Client
  -> Cloudflare Quick Tunnel
    -> Azure Linux VM
      -> Cloud Gateway (port 8080)
      -> LobeChat Docker container (port 3210)
      -> Cloud Drive Python service (127.0.0.1:8787)
      -> systemd and cloudflared service management
      -> local data directories and environment files
```

### AI 对话路径 | AI Chat Path

用户输入消息 -> LobeChat 前端 -> Node.js 后端 -> 对应模型供应商 API -> 流式返回响应
User message -> LobeChat frontend -> Node.js backend -> provider API -> streamed response

### 云盘路径 | Cloud Drive Path

浏览器打开云盘 -> Python 后端读取目录 -> 前端渲染文件树 -> 用户上传文件 -> 保存到存储目录 -> 刷新列表
Browser opens cloud drive -> Python backend reads directories -> frontend renders file tree -> user uploads files -> files are saved -> list refreshes

### 为什么这样分层 | Why the Stack Is Split This Way

- 前端和后端分离，便于维护不同的职责边界。
- Frontend and backend are separated so each component keeps a clear responsibility.
- 云盘服务只暴露必要接口，降低无关风险面。
- The cloud drive service exposes only the required interfaces to reduce risk.
- AI 对话和文件管理共用一台主机，但各自独立运行。
- AI chat and file management share one host while still running independently.

---

## 目录结构 | Repository Layout

| 路径 | 作用 | 说明 |
|------|------|------|
| README.md | 根目录说明 | 主入口文档，概览整个项目 |
| my-project/README.md | 子项目说明 | 更偏实现细节和部署背景 |
| my-project/cloud_drive_server.py | 云盘后端 | Python 云盘服务入口 |
| my-project/cloud-drive.service | systemd 服务 | 云盘服务的守护配置 |
| my-project/mkdocs.yml | 文档配置 | MkDocs 站点构建配置 |
| my-project/docs/ | 文档源文件 | GitHub Pages 的内容来源 |
| my-project/docs/stylesheets/extra.css | 自定义样式 | 文档站点样式扩展 |
| my-project/site/ | 静态站点输出 | 构建后的文档页面 |
| my-project/requirements.txt | Python 依赖 | 云盘服务所需包 |

---

## 核心配置 | Core Configuration

### LobeChat 环境变量 | LobeChat Environment

- NODE_ENV=production：生产模式。
- NODE_ENV=production: production mode.
- HOSTNAME=0.0.0.0：监听所有网卡。
- HOSTNAME=0.0.0.0: listen on all interfaces.
- PORT=3210：LobeChat 端口。
- PORT=3210: LobeChat port.
- *_API_KEY：用户或预配置的密钥。
- *_API_KEY: user or preconfigured keys.
- *_MODEL_LIST：可留空，支持动态获取模型列表。
- *_MODEL_LIST: can be left empty when dynamic model fetching is enabled.

### Cloud Drive 服务 | Cloud Drive Service

- 监听地址：127.0.0.1:8787。
- Listen address: 127.0.0.1:8787.
- 根目录：/home/azureuser/cloud-drive。
- Root directory: /home/azureuser/cloud-drive.
- systemd 负责后台常驻和自动重启。
- systemd keeps the service running and restarts it automatically.

### 隧道与发布 | Tunnel and Publishing

- Cloudflare Tunnel 把本地服务映射到公网地址。
- Cloudflare Tunnel maps local services to public URLs.
- GitHub Pages 负责展示文档站点。
- GitHub Pages hosts the documentation site.
- 站点内容由 MkDocs 从 docs 目录生成。
- The site content is generated by MkDocs from the docs directory.

---

## 部署流程 | Deployment Flow

1. 准备一台 Linux 主机或 Azure VM，安装 Docker、Python 3.11+、Git、systemd 和 Cloudflare Tunnel 客户端。 / Prepare a Linux host or Azure VM, then install Docker, Python 3.11+, Git, systemd, and the Cloudflare Tunnel client.
2. 配置 LobeChat 的环境变量，确保模型供应商的 API 密钥可用。 / Configure the LobeChat environment variables and make sure provider API keys are available.
3. 启动 LobeChat 容器，让 AI 对话页面通过 3210 端口运行。 / Start the LobeChat container so the AI chat page runs on port 3210.
4. 配置并启用 cloud_drive_server.py 对应的 systemd 服务。 / Configure and enable the systemd service for cloud_drive_server.py.
5. 将 Cloudflare Tunnel 指向本地服务，让外网可以访问两个入口。 / Point Cloudflare Tunnel at the local services so both endpoints are publicly reachable.
6. 构建 MkDocs 文档并推送到 GitHub Pages。 / Build the MkDocs docs and publish them through GitHub Pages.

---

## 维护建议 | Operations and Maintenance

- 把密钥放在环境文件里，不要提交到仓库。
- Keep secrets in environment files and do not commit them to the repository.
- 定期备份云盘根目录，避免文件误删或主机故障造成损失。
- Back up the cloud drive root directory regularly to avoid data loss from mistakes or host failures.
- 通过 systemd 日志和服务状态排查启动问题。
- Use systemd logs and service status to troubleshoot startup issues.
- 访问地址变更时，及时更新 README 和文档站点。
- Update the README and docs site whenever access URLs change.
- 如果需要调整样式，优先修改 docs/stylesheets/extra.css。
- If you need visual changes, prefer updating docs/stylesheets/extra.css first.
- 根目录 README 作为总入口，子目录 README 适合放更细的实现说明。
- Keep the root README as the landing page and use the subproject README for implementation details.

---

## 支持的供应商 | Supported Providers

主流模型源包括 OpenRouter、OpenAI、Anthropic、Google Gemini、Mistral AI、Groq、DeepSeek、Perplexity 和 Cohere。

Main providers include OpenRouter, OpenAI, Anthropic, Google Gemini, Mistral AI, Groq, DeepSeek, Perplexity, and Cohere.

其他供应商还包括 AI21、Baichuan、Azure、Hugging Face、Ollama、Qwen、Wenxin、Spark 等。

Other providers also include AI21, Baichuan, Azure, Hugging Face, Ollama, Qwen, Wenxin, Spark, and more.

不同供应商的可用性取决于 API 密钥、地区限制和当前平台支持情况。
Provider availability depends on API keys, region restrictions, and current platform support.

---

## 常见问题 | FAQ

### 为什么模型列表为空？ | Why is the model list empty?

通常是因为 API 密钥未配置、供应商接口暂时不可用，或者网络无法访问对应服务。
This is usually caused by a missing API key, a temporarily unavailable provider API, or network access issues.

### 为什么云盘上传失败？ | Why does a cloud drive upload fail?

先检查上传密码、目录权限和云盘根目录是否存在，再看 systemd 日志是否有报错。
Check the upload password, directory permissions, and whether the cloud drive root exists, then inspect the systemd logs for errors.

### 为什么 GitHub Pages 没有更新？ | Why is GitHub Pages not updated?

通常需要重新构建 MkDocs 站点，并确认最新提交已经推送到主分支。
You usually need to rebuild the MkDocs site and confirm the latest commit has been pushed to the main branch.

---

## 相关链接 | Related Links

- 项目主页 / Project home: https://sihan-bzwj.github.io/-sihan-bzwj-.github.io/
- 仓库地址 / Repository: https://github.com/sihan-bzwj/-sihan-bzwj-.github.io
- Cloud Drive 页面 / Cloud Drive page: https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive
- LobeChat 文档 / LobeChat docs: https://docs.lobehub.com/

---

## 版本说明 | Version Notes

这份 README 的重点是把项目整体结构、在线入口、核心功能和维护方式讲清楚，方便后续持续更新。
The purpose of this README is to explain the overall structure, live entrypoints, core features, and maintenance approach clearly so future updates stay manageable.

---

## 附录 A | Deployment Checklist

- 基础环境检查：先确认主机时间同步、磁盘剩余空间、DNS 解析和出站网络都正常；这些基础条件一旦不稳，Docker、GitHub Pages 和 Cloudflare Tunnel 的问题会互相干扰，排查成本会快速上升。 / Basic environment check: verify host time sync, disk headroom, DNS resolution, and outbound networking first; when these basics are unstable, Docker, GitHub Pages, and Cloudflare Tunnel issues interfere with each other and diagnosis gets much harder.
- 目录准备：确认 `/home/azureuser/cloud-drive`、`my-project/docs/` 和静态站点输出目录都已存在，权限与执行用户一致，避免后续因为路径不存在或所有权不一致导致服务启动失败。 / Directory prep: make sure `/home/azureuser/cloud-drive`, `my-project/docs/`, and the static site output path exist with matching ownership and permissions so later service starts do not fail due to missing paths or mismatched owners.
- 密钥管理：把所有 API 密钥、上传密码和环境变量都放到单独的配置文件中，仓库只保留模板或说明，不要把真实秘密写进提交记录，这样回滚和迁移都会更安全。 / Secret management: keep API keys, upload passwords, and environment variables in dedicated config files; the repository should only contain templates or instructions, never real secrets, so rollbacks and migrations stay safe.
- 版本控制：在改动 README、MkDocs 和服务配置之前先确认 `git status` 是干净的，修改后先看差异再提交，避免把临时调试内容、截图路径或旧地址混进正式文档。 / Version control: before changing README, MkDocs, or service configs, confirm `git status` is clean; after editing, review the diff before committing so temporary debugging content, screenshot paths, or stale URLs do not leak into the official docs.
- 依赖准备：确保 `Docker`、`Python 3.11+`、`Git`、`systemd` 和 `cloudflared` 都已安装并可用，必要时先做最小化启动测试，再继续进行应用配置，这样能尽早暴露平台问题。 / Dependency prep: ensure `Docker`, `Python 3.11+`, `Git`, `systemd`, and `cloudflared` are installed and usable; if needed, run a minimal startup test first so platform issues surface early.
- 端口规划：LobeChat 维持在 `3210`，Cloud Gateway 维持在 `127.0.0.1:8080`，云盘服务维持在 `127.0.0.1:8787`，对外只通过 Cloudflare Tunnel 暴露，不要额外开放多余端口，以免把内部服务直接暴露给公网。 / Port planning: keep LobeChat on `3210`, the Cloud Gateway on `127.0.0.1:8080`, and the cloud drive service on `127.0.0.1:8787`; expose them externally only through Cloudflare Tunnel and avoid opening extra ports that would expose internal services to the public Internet.
- 文档源与生成物：`my-project/docs/` 保存源文档，`my-project/site/` 保存构建结果，编辑时只改源文档，发布前再构建生成物，避免把产物当成源文件一起维护。 / Source vs generated docs: `my-project/docs/` stores source content and `my-project/site/` stores generated output; edit only the source docs and rebuild before publishing so generated artifacts are not treated as source files.
- 提交粒度：每次只处理一个明确主题，例如只改 README、只改云盘配置或只改 MkDocs 样式，这样在审查历史和回滚时更容易定位变化，也更容易确认问题来源。 / Commit granularity: handle one clear topic at a time, such as only README, only cloud drive config, or only MkDocs styling; this makes history review and rollback simpler and makes root cause analysis easier.
- 联动验证：改完任意一处后，都要同时验证本地文件、浏览器展示和远端页面，因为一个链接、一个标题或一个样式都可能在不同层面呈现不同结果。 / Cross-layer verification: after editing anything, verify the local file, browser rendering, and remote page together because one link, heading, or style can behave differently across layers.
- 公开地址维护：Cloudflare Quick Tunnel 的地址是可变资源，遇到重建或切换时要同步更新 README、文档页和任何截图注释，不要保留旧地址让用户误访问。 / Public URL maintenance: Cloudflare Quick Tunnel URLs are mutable; when the tunnel is recreated or changed, update README, the docs site, and any screenshot captions so users do not follow stale links.
- 访问权限：如果需要增加新的读写能力，优先检查是否能通过现有服务和权限模型完成，不要先放开整机权限，避免把单一功能扩展成全局风险。 / Access control: when adding new read/write capability, first check whether the existing services and permission model already support it; do not broaden host-wide permissions too early or a single feature can become a global risk.
- 页面一致性：根目录 README 负责讲清楚项目全貌，`my-project/README.md` 负责更偏实现和部署细节，两者内容要保持一致但不要完全重复。 / Page consistency: the root README should explain the overall project while `my-project/README.md` should focus on implementation and deployment details; keep them aligned without duplicating everything.
- 备份基线：至少保留一份能恢复当前工作状态的备份，包括环境文件、服务文件和文档源文件，必要时先备份再调整，避免回滚时发现缺少关键配置。 / Backup baseline: keep at least one recoverable backup of the current state, including environment files, service files, and source docs; back up first when in doubt so rollbacks do not fail because critical config is missing.
- 浏览器验证：每次修改首页、链接或样式后都在浏览器里刷新验证，确认标题、表格、链接和段落折行都符合预期，避免只看文本却忽略最终渲染效果。 / Browser verification: after changing a homepage, link, or style, refresh it in the browser and confirm the title, tables, links, and wrapping all render as expected instead of relying on raw text only.
- 回滚策略：如果某次变更影响到线上可访问性，优先回退最小范围的文件而不是整仓库重置，这样可以保留已验证的稳定部分，只撤销真正出问题的那一块。 / Rollback strategy: if a change affects online availability, roll back the smallest possible file set rather than resetting the whole repo so already validated stable parts remain intact.
- 依赖更新：在升级 Python 包、Docker 镜像或前端依赖前，先确认文档和服务配置是否依赖旧行为，升级后再检查启动日志与页面输出，避免隐性破坏。 / Dependency updates: before upgrading Python packages, Docker images, or frontend dependencies, verify whether docs or service configs rely on old behavior; after the upgrade, inspect startup logs and page output to catch hidden breakage.
- 记录约定：把 URL、端口、根目录、默认服务名和常用命令写在 README 中，后续维护者能直接从文档恢复上下文，不必再翻历史提交找答案。 / Recording conventions: write URLs, ports, root directories, default service names, and common commands in the README so future maintainers can recover context from the docs instead of searching commit history.
- 变更优先级：遇到展示问题时先处理可见错误，再处理配置和结构性问题；用户通常先看到错误内容或错误链接，因此第一步应当让页面恢复可用。 / Change priority: when facing a presentation issue, fix the visible error first and the configuration or structural issue second; users notice broken content or links first, so restore usability before deeper cleanup.
- 维护节奏：如果只是链接变化或措辞调整，直接修改 README；如果牵涉服务行为、端口或权限，先在子项目里验证，再同步回根目录文档。 / Maintenance cadence: if the change is only a link or wording update, edit the README directly; if it affects service behavior, ports, or permissions, validate it in the subproject first and then sync the root docs.
- 说明边界：README 应该把入口、结构、流程和风险讲清楚，但不应该把每个底层实现细节都写进去；更细的代码级信息留给子项目文档或代码注释。 / Scope boundary: the README should explain entry points, structure, flow, and risks, but it should not include every low-level implementation detail; leave code-level detail for subproject docs or code comments.
- 命名一致性：页面标题、仓库名、Cloudflare 路径和 GitHub Pages 路径尽量保持一致，减少用户在多个入口之间跳转时产生的认知负担。 / Naming consistency: keep page titles, repo names, Cloudflare paths, and GitHub Pages paths aligned so users do not have to build a new mental model for every entry point.
- 样式修改：如果需要调整阅读体验，优先修改 `docs/stylesheets/extra.css`，先小范围验证字体、间距和表格样式，再决定是否扩展到更多页面。 / Style changes: when adjusting readability, prefer `docs/stylesheets/extra.css`, validate fonts, spacing, and table styles in a small scope first, and only then expand to more pages.
- 目录权限：云盘根目录的所有者和运行服务的用户必须一致或具备明确读写权限，否则上传和目录遍历很容易在看似正常的情况下失败。 / Directory permissions: the cloud drive root owner and the service runtime user must match or have explicit read/write permissions; otherwise uploads and directory traversal can fail even when everything looks normal.
- 网页缓存：遇到内容已经更新但浏览器仍显示旧页面时，先做强制刷新和无痕窗口验证，再判断是不是发布链路真的没生效。 / Browser cache: if content is updated but the browser still shows an old page, force refresh and verify in an incognito window before deciding the publishing chain truly failed.
- 日志优先：任何服务问题都先看日志，再改配置；日志能直接告诉你是路径、权限、端口、依赖还是网络问题，通常比猜测更快定位。 / Logs first: for any service issue, inspect logs before changing config; logs usually reveal whether the problem is path, permission, port, dependency, or network related and are much faster than guessing.

## 附录 B | Runtime Notes

- LobeChat 启动顺序：先确认环境变量和 API 密钥，再启动容器，然后验证模型列表与流式输出是否正常，最后再开放给外部访问，这样可以把“能启动”和“能正确工作”分开验证。 / LobeChat start order: confirm environment variables and API keys first, then start the container, verify model lists and streaming output, and only then expose it publicly so “starts” and “works correctly” are validated separately.
- LobeChat 运行策略：把后端代理视为唯一可信出口，前端只负责交互和展示，不直接保存敏感信息，也不把密钥写到静态资源里，避免把认证面扩散到浏览器。 / LobeChat runtime policy: treat the backend proxy as the only trusted exit, keep the frontend for interaction and presentation only, and never store secrets in static assets so the authentication surface does not spread into the browser.
- 模型供应商维护：新增或更换供应商时，先检查平台支持、密钥格式和地区限制，再更新模型列表逻辑；如果某个供应商有动态列表接口，优先用动态获取，降低手工维护成本。 / Provider maintenance: when adding or switching providers, check platform support, key format, and region restrictions first, then update model list logic; if a provider supports dynamic model lists, prefer that to reduce manual maintenance.
- 云盘启动顺序：先准备虚拟环境和依赖，再确认根目录、权限和密码，接着启动 `cloud_drive_server.py` 或对应 systemd 服务，最后从浏览器验证目录树、上传和下载是否正常。 / Cloud drive start order: prepare the virtual environment and dependencies first, confirm the root directory, permissions, and password next, then start `cloud_drive_server.py` or its systemd service, and finally verify the tree view, uploads, and downloads in the browser.
- 云盘服务边界：云盘进程只负责文件操作和页面输出，不应该承担和 AI 对话平台无关的任务；如果以后要扩展功能，先判断是否需要拆成独立模块，而不是往单个脚本里不断堆叠逻辑。 / Cloud drive boundaries: the cloud drive process should handle file operations and page output only, not unrelated AI chat responsibilities; if future features grow, first decide whether to split into modules instead of piling everything into one script.
- systemd 管理：服务文件的作用是把启动、重启、日志和依赖关系固定下来，所以变更服务文件后一定要 `systemctl daemon-reload` 再重启服务，避免旧配置继续生效。 / systemd management: the service file exists to pin startup, restart, logs, and dependencies, so after changing it always run `systemctl daemon-reload` before restarting or the old config may still be active.
- Cloudflare Tunnel 行为：隧道更多是“地址映射层”而不是“应用层”，因此应用问题要先在本机和局域网排掉，再去看隧道配置是否正确，不要把所有故障都归因于公网入口。 / Cloudflare Tunnel behavior: the tunnel is an address-mapping layer rather than an application layer, so fix local and LAN issues first and only then check tunnel config; do not blame every failure on the public entry point.
- 网络与端口：对外暴露的服务越少越好，内网端口尽量保留在本地回环或受限网络里，外部访问只通过一个清晰的入口层转发，便于安全审查和故障排查。 / Network and ports: the fewer exposed services the better; keep internal ports on loopback or restricted networks where possible and forward external access through a clear entry layer for easier security review and troubleshooting.
- 浏览器验证：每次改完配置都要在浏览器里真实访问一次，而不是只看静态文件是否存在；页面标题、按钮、表格和路径前缀都属于用户可见状态，必须在最终入口上确认。 / Browser validation: after each config change, actually visit it in a browser instead of only checking whether static files exist; page titles, buttons, tables, and path prefixes are user-visible state and must be confirmed at the final entry point.
- 日志位置：如果服务由 systemd 管理，优先用 `journalctl -u <service>` 看日志；如果是容器或脚本启动，再结合 `docker logs` 或进程输出判断错误来源，不要只看一个层级的消息。 / Log location: if a service is managed by systemd, use `journalctl -u <service>` first; if it is containerized or script-based, combine it with `docker logs` or process output rather than relying on just one log source.
- 重启策略：在修改依赖、配置文件或模板之后，重启服务比盲目刷新页面更重要，因为缓存和旧进程都会掩盖真正的运行状态。 / Restart strategy: after changing dependencies, config files, or templates, restarting the service is more important than blindly refreshing the page because caches and stale processes can hide the real runtime state.
- 数据隔离：代码仓库、配置文件、运行数据和构建产物应该分开管理，尤其是 `docs/`、`site/` 和云盘数据目录，不要混在同一层级造成误删。 / Data separation: code, configuration, runtime data, and build artifacts should be managed separately, especially `docs/`, `site/`, and the cloud drive data directory, so they are not mixed at the same level and accidentally deleted.
- 运行状态：如果页面能打开但功能异常，先判断是展示层、接口层还是存储层的问题；如果页面都打不开，先从端口、隧道和服务状态查起，别急着改业务逻辑。 / Runtime state: if the page opens but features are broken, first decide whether it is a presentation, API, or storage issue; if the page does not open at all, start with ports, tunnel, and service state before changing business logic.
- 临时修改：调试阶段可以临时改配置，但在问题解决后要把临时改动收回到文档里，避免“能跑但不可维护”的状态持续存在。 / Temporary edits: during debugging you may change config temporarily, but once the issue is solved, fold the temporary change back into the docs so the system does not remain in a “works, but not maintainable” state.
- 入口一致：如果 Cloudflare Tunnel、GitHub Pages 和仓库页面都存在，三者展示的项目名、标题和描述尽量保持一致，减少用户在多个入口间切换时的困惑。 / Entry consistency: if Cloudflare Tunnel, GitHub Pages, and the repo page all exist, keep the project name, title, and description aligned across them so users are less confused when switching between entry points.
- 读写路径：云盘的读写路径一旦改变，就要同步更新页面文案和示例路径；不要让用户看到和实际目录结构不一致的说明，这会直接增加误操作概率。 / Read/write paths: if the cloud drive path changes, update page copy and sample paths immediately; do not leave users with instructions that conflict with the actual directory structure because that increases the chance of mistakes.
- 维护记录：如果某次修改修复了特定故障，最好把故障现象、原因和修复方式补进 README 或子项目 README，下一次遇到相同问题时就能直接复用经验。 / Maintenance notes: when a change fixes a specific issue, add the symptom, cause, and fix to the README or subproject README so the next time the same problem appears you can reuse the solution quickly.
- 文档粒度：根目录文档适合放总览、入口和维护约定，子项目文档适合放具体实现和操作步骤；两者配合比把所有内容塞进一个文件更容易长期维护。 / Documentation granularity: the root README should cover the overview, entry points, and maintenance conventions, while subproject docs should cover implementation and operational steps; keeping them separate is easier to maintain than stuffing everything into one file.
- 访问验证：改完任何链接之后，都要从浏览器里点过去确认一次，尤其是 GitHub Pages 和 Cloudflare 地址；文本看起来没问题，不代表点击后真的能到。 / Access validation: after changing any link, click it in the browser to confirm it works, especially GitHub Pages and Cloudflare URLs; text looking fine does not mean the link actually resolves.
- 资源清理：调试结束后及时清理无用的中间产物、临时文件和旧链接记录，保持仓库和运行目录干净，这样后续排错不会被历史垃圾干扰。 / Cleanup: after debugging, remove unused intermediates, temporary files, and stale link records so the repo and runtime directories stay clean and future troubleshooting is not polluted by old clutter.
- 维护频率：如果项目地址、服务端口或页面结构发生变化，尽量在同一次提交里同时更新 README、子项目说明和文档站点，避免不同文档在不同时间点互相矛盾。 / Maintenance frequency: when project URLs, service ports, or page structure change, update the README, subproject docs, and docs site in the same commit if possible so the documents do not drift apart.
- 交付标准：真正交付给用户的不是“代码已经改了”，而是“文档、页面和运行状态都能指向同一个事实”；这份 README 的作用就是把这些事实固定下来。 / Delivery standard: what you deliver is not merely “the code changed,” but “the docs, pages, and runtime state all point to the same facts”; this README exists to anchor those facts.

## 附录 C | Docs Publishing

- 源文档位置：`my-project/docs/` 是 MkDocs 的源输入目录，改这里才是修改站点内容的正确方式；`site/` 是生成产物，通常不应手工编辑，因为它会被下一次构建覆盖。 / Source docs location: `my-project/docs/` is the MkDocs input directory, so editing here is the correct way to change site content; `site/` is generated output and should normally not be edited by hand because the next build will overwrite it.
- 主页与导航：`my-project/mkdocs.yml` 负责定义导航、主题和插件，改导航前先确认页面层级和标题是否一致，否则浏览目录时会出现同名页面或断层。 / Homepage and navigation: `my-project/mkdocs.yml` defines navigation, theme, and plugins; before changing it, verify page hierarchy and titles so browsing does not produce duplicate names or dead ends.
- 样式扩展：自定义样式优先放在 `my-project/docs/stylesheets/extra.css`，这样主题升级时更容易保留局部定制，也能把页面气质控制在统一范围内。 / Style extensions: put custom styles in `my-project/docs/stylesheets/extra.css` first so theme upgrades preserve local customizations and the page tone stays consistent.
- 构建验证：每次发布前都要先本地构建一次站点，确认首页、目录、代码块和表格没有跑版，再决定是否推送；先在本地发现问题，比到线上再修正成本低得多。 / Build validation: before publishing, build the site locally and confirm the homepage, nav, code blocks, and tables are not broken, because catching issues locally is much cheaper than fixing them online.
- 发布节奏：如果只是文字修订，可以单独提交文档；如果牵涉到链接、页面结构或样式调整，建议连 README 一起改，这样 GitHub Pages、仓库首页和子项目页的叙述会同步。 / Release cadence: if only text changes, submit the docs alone; if links, structure, or style changes are involved, update the README together so GitHub Pages, the repo home, and subproject pages stay aligned.
- 链接同步：项目主页、仓库地址、云盘入口和文档入口一旦变化，所有互相引用的链接都要一起改，否则用户从一个页面跳到另一个页面时会遇到旧地址。 / Link sync: when the project home, repo URL, cloud drive entry, or docs entry changes, update all cross-references at once so users do not hit stale links when moving between pages.
- 图片和徽章：如果后续要加截图或状态徽章，先确认这些外链长期稳定，再放进 README 或文档首页；临时图片最好放在可控仓库中，而不是散落在不可控的个人图床里。 / Images and badges: if you add screenshots or status badges later, make sure the external links are stable before putting them in README or the docs homepage; temporary images are best kept in a controlled repo rather than scattered across unpredictable personal image hosts.
- 结构层次：文档应当先说明“是什么”，再说明“怎么访问”，接着说明“怎么运行”，最后说明“怎么维护”；这个顺序最符合用户浏览习惯，也最容易在快速扫描时找到答案。 / Structural hierarchy: docs should explain “what it is,” then “how to access it,” then “how to run it,” and finally “how to maintain it”; that order matches how people scan pages and makes answers easier to find quickly.
- 语言风格：中英双语不需要逐字对齐，但需要在每个核心段落里同时表达同一个事实，这样读者不会因为翻译差异而误解部署范围或运维边界。 / Language style: bilingual content does not need word-for-word alignment, but each core section should express the same fact in both languages so readers do not misread scope or boundaries because of translation drift.
- 页面验收：如果 GitHub Pages 页面上看起来正常，就再在移动端和桌面端各验证一次；有些表格在窄屏上会折行，必须确认折行后信息仍然可读。 / Page acceptance: if the GitHub Pages page looks fine, verify it once on both mobile and desktop; some tables wrap on narrow screens, so check that the wrapped text remains readable.
- 建议保留：文档中关于访问地址、端口、目录和服务文件的说明最好长期保留，即使实现方式变化，这些“操作入口”通常是最先被维护者查找的内容。 / Keep these notes: keep the docs for access URLs, ports, directories, and service files around long term because, even if implementation changes, these operational entry points are usually the first things maintainers look for.

## 附录 D | Routine Maintenance

- 日常检查：每天或每次发布后，快速看一眼 systemd 状态、容器状态、浏览器页面和 GitHub Pages 结果，确认它们仍然指向同一个可用版本。 / Daily check: after each publish, quickly review systemd status, container status, browser page, and GitHub Pages output to confirm they still point to the same working version.
- 备份节奏：云盘数据目录、环境文件和服务文件应当按固定节奏备份；如果这些东西丢了，恢复工作会比修一个网页复杂得多。 / Backup rhythm: back up the cloud drive data directory, environment files, and service files on a fixed schedule; losing them makes recovery much harder than fixing a web page.
- 依赖更新：升级 Python 包、Docker 镜像或前端依赖前，先确认文档里有没有写死版本假设；升级之后再重新构建并验证一次，避免“能装上但不能跑”。 / Dependency updates: before upgrading Python packages, Docker images, or frontend dependencies, check whether the docs assume fixed versions; after upgrading, rebuild and verify again so “installed but not runnable” does not happen.
- 日志阅读：日志是排障第一入口，看到错误后先判断是路径、权限、网络、端口还是配置格式问题，再决定是不是要改代码。 / Log reading: logs are the first debugging entry point; when errors appear, decide first whether the issue is path, permission, network, port, or config format related before changing code.
- 证书与隧道：如果以后加入更多公开入口，要把证书、隧道和访问路径统一管理，不要让同一项目里出现多个不同来源的公网地址而无人维护。 / Certificates and tunnels: if more public endpoints are added later, manage certificates, tunnels, and access paths together so the same project does not accumulate multiple unmanaged public URLs.
- 目录清理：保持 `docs/`、`site/`、`cloud-drive/` 和工作目录整洁，定期清理废弃文件和旧截图，避免在查找真实问题时被历史产物干扰。 / Directory cleanup: keep `docs/`, `site/`, `cloud-drive/`, and the workspace tidy, and periodically remove stale files and screenshots so historical artifacts do not distract from real issues.
- 变更记录：对用户可见的改动最好在 README 或子项目 README 中留一条简短说明，比如链接迁移、端口调整或服务方式变化，这样后续能快速对照历史。 / Change notes: for user-visible changes, leave a short note in the README or subproject README, such as URL migrations, port changes, or service model updates, so later comparisons are easy.
- 性能感知：如果页面变慢，先判断是前端资源、模型供应商、云盘目录枚举还是隧道延迟，不要把所有慢速都归到同一个原因上。 / Performance awareness: if the page feels slow, first distinguish frontend assets, provider latency, cloud drive enumeration, and tunnel delay instead of attributing every slowdown to a single cause.
- 访问审计：如果未来增加用户权限或下载审计，建议优先把规则放在后端或服务层，不要把控制逻辑散落在前端页面里。 / Access auditing: if user permissions or download auditing are added later, place the rules in the backend or service layer rather than scattering control logic across the frontend.
- 回归验证：每次改完文档后，至少点击一次所有关键链接，确认根目录 README、项目主页、云盘入口和 LobeChat 文档都能正常打开。 / Regression verification: after each documentation update, click every critical link at least once to confirm the root README, project home, cloud drive entry, and LobeChat docs all open correctly.
- 维护目标：让一个新的维护者只看 README 就能知道系统由什么组成、入口在哪里、配置放哪儿、出错后从哪开始查。 / Maintenance goal: a new maintainer should be able to read the README and understand what the system is, where the entry points are, where config lives, and where to start when things break.

## 附录 E | Troubleshooting

- 模型列表为空：先检查 API 密钥是否真的写入环境变量，再确认供应商接口是否可用，最后看前端选择的 provider 是否和密钥对应；很多“空列表”其实是配置未加载。 / Empty model list: first check whether the API key is actually in the environment, then whether the provider API is available, and finally whether the frontend provider choice matches the key; many “empty list” cases are simply config not loaded.
- 云盘上传失败：优先确认上传密码、目录权限和根目录存在性，再看文件名是否包含不兼容字符；如果服务端权限没问题，往往就是浏览器请求或路径映射出了偏差。 / Upload failure: first confirm the upload password, directory permissions, and root directory existence, then check whether the file name contains unsupported characters; if server permissions are fine, the issue is often browser request or path mapping related.
- 页面 404：如果项目主页或云盘页面返回 404，先确认 Cloudflare Tunnel 的转发路径、GitHub Pages 的发布状态和文档站点的路由规则是否一致，不要先怀疑页面文本本身。 / 404 page: if the project home or cloud drive page returns 404, first confirm the Cloudflare Tunnel forwarding path, GitHub Pages publish status, and docs routing rules are consistent; do not blame the page text first.
- 容器未启动：如果 LobeChat 容器起不来，先看端口冲突、环境变量缺失和镜像是否存在，再看应用日志；容器层的问题通常比业务层问题更早暴露。 / Container not starting: if the LobeChat container will not start, check port conflicts, missing environment variables, and whether the image exists, then inspect app logs; container issues usually surface before business logic issues.
- systemd 失败：如果云盘服务的 systemd 单元启动失败，先检查 `ExecStart`、工作目录和用户权限，再确认 Python 虚拟环境是否已经准备好。 / systemd failure: if the cloud drive service unit fails, check `ExecStart`, working directory, and user permissions first, then confirm the Python virtual environment is ready.
- 隧道异常：如果公网地址能打开但内容不对，优先检查本地服务是否真的返回了预期内容，而不是只盯着隧道本身；隧道只是转发，应用仍然是根因。 / Tunnel anomaly: if the public address opens but the content is wrong, check whether the local service actually returns the expected content instead of focusing only on the tunnel; the tunnel only forwards traffic, the app is still the root cause.
- 样式错乱：如果 GitHub Pages 里表格或标题样式异常，先确认 `extra.css` 和主题文件是否同时被改动，然后再检查浏览器缓存；样式问题经常是版本不同步造成的。 / Style corruption: if tables or headings look broken on GitHub Pages, first confirm whether `extra.css` and theme files were changed together, then check browser cache; style issues are often caused by version drift.
- 路由不一致：如果根目录 README、GitHub Pages 和服务入口对同一页面给出了不同路径，先统一对外链接，再回头调整内部实现；对用户来说，链接一致性比内部结构更重要。 / Route mismatch: if the root README, GitHub Pages, and service entry use different paths for the same page, unify the public links first and adjust internals later; for users, link consistency matters more than internal layout.
- 浏览器缓存：当内容已经更新但浏览器仍显示旧页面时，先做强制刷新或无痕窗口验证，再判断是否真的没有发布成功；不要把缓存问题误判成构建失败。 / Browser cache: when content has updated but the browser still shows an old page, force refresh or use an incognito window before concluding publish failed; do not misread cache issues as build failures.
- 权限不匹配：如果上传、删除或重命名偶尔成功偶尔失败，八成是目录权限、文件所有者或运行用户不一致；把权限和所有权统一后问题通常会明显减少。 / Permission mismatch: if upload, delete, or rename operations succeed inconsistently, the likely cause is directory permissions, file ownership, or runtime user mismatch; fixing ownership and permissions usually reduces the issue dramatically.
- 日志缺失：如果你看不到足够的日志，先把日志级别调高再复现问题；没有日志的系统只能靠猜，而猜测很难稳定定位。 / Missing logs: if you do not have enough logs, raise the log level and reproduce the issue; a system without logs forces guesswork, and guesswork is not reliable.
- 多点验证：故障排查时至少从三个层面看同一个问题：本地配置、服务输出和浏览器结果；三个层面都对上了，问题才算真的被修好。 / Multi-point verification: when troubleshooting, inspect the same issue from at least three layers: local config, service output, and browser result; the issue is truly fixed only when all three agree.

## 附录 F | Rollback and Recovery

- 最小回滚：如果某次改动引入问题，优先回退单个文件或单个段落，不要整仓库硬回滚；这样可以保留已经验证过的好内容，只撤销真正出问题的那部分。 / Minimal rollback: if a change introduces a problem, roll back a single file or section instead of the entire repo; that preserves already validated good content and removes only the broken part.
- 恢复顺序：先恢复能让页面回到可访问状态的内容，再恢复说明文档和优化项；可用性优先于美观，先让用户能打开，再让用户看得更舒服。 / Recovery order: first restore the content that makes the page accessible, then restore docs and polish; usability comes before aesthetics, so make it open first and prettier second.
- 备份验证：恢复之前先确认备份文件真的包含你想要的版本，而不是只看文件名；对于 README、服务文件和文档站点，内容是否正确比备份日期更关键。 / Backup verification: before restoring, confirm the backup actually contains the version you want rather than trusting the filename; for README, service files, and docs, the content matters more than the backup date.
- 链接回滚：如果链接或地址改错了，先把最明显的错误链接恢复正确，再检查其他引用；很多时候一个旧链接会在多个页面里连锁出现。 / Link rollback: if a link or address is changed incorrectly, fix the most obvious broken link first and then check other references; a single stale link often propagates across multiple pages.
- 文档回滚：如果 README 的某一段写得不清楚，回滚到清晰版本后再做局部重写，不要在一个混乱版本上不断叠加补丁。 / Docs rollback: if a README section becomes unclear, roll back to the clear version and rewrite locally instead of stacking patches on top of a messy version.
- 服务回滚：如果云盘或 LobeChat 的配置升级导致异常，优先回退配置文件，再回退镜像或依赖版本；把变化范围缩小，通常更容易找出真正原因。 / Service rollback: if an upgrade to cloud drive or LobeChat config causes issues, roll back the config file first and then image or dependency versions; narrowing the change scope usually reveals the real cause faster.
- 路由回滚：如果 Cloudflare Tunnel 或 GitHub Pages 路由改错，先恢复对外入口，再去整理内部路径；对外入口是用户最先接触到的东西。 / Route rollback: if Cloudflare Tunnel or GitHub Pages routing is changed incorrectly, restore the public entry first and then clean up internal paths; the public entry is the first thing users encounter.
- 结构回滚：如果文档结构被改乱了，先把章节恢复成“概览 -> 入口 -> 功能 -> 架构 -> 配置 -> 维护 -> 链接”的顺序，再补充细节；这个骨架最不容易迷路。 / Structural rollback: if the document structure gets messy, restore the order to “overview -> access -> features -> architecture -> config -> maintenance -> links” first, then add details; this skeleton is easiest to navigate.
- 历史对照：回滚时不要只看最新提交，也要看前一个稳定版本的 diff，这样能快速判断是某次新增内容的问题，还是之前就已经存在的结构性缺陷。 / History comparison: during rollback, look not only at the latest commit but also at the diff of the previous stable version so you can quickly tell whether the issue came from a new change or an older structural problem.
- 验收恢复：恢复完成后必须重新访问一次主页、云盘、GitHub Pages 和仓库页面，确认它们都回到同一个稳定版本，不要只看本地文件就宣布完成。 / Recovery validation: after restoration, revisit the home page, cloud drive, GitHub Pages, and repo page to confirm they all returned to the same stable version; do not declare success based on local files alone.
- 经验沉淀：每次回滚成功后，把原因和修复写进附录或子项目 README，下一次遇到相似故障时，就能直接复制正确的排查顺序。 / Knowledge capture: after a successful rollback, record the cause and fix in the appendix or subproject README so you can reuse the correct troubleshooting sequence the next time a similar issue appears.

## 附录 G | Security Boundaries

- 最小暴露：公网只暴露必须暴露的入口，云盘服务和 LobeChat 后端都尽量放在受控转发后面；如果某个端口没有业务价值，就不要让它出现在公网。 / Minimal exposure: expose only the public entry points that are necessary, and keep the cloud drive and LobeChat backend behind controlled forwarding; if a port has no business value, do not put it on the public Internet.
- 密钥边界：API 密钥、上传密码和管理口令都应该留在服务端或环境文件里，不要写进前端、截图或公开日志，因为这些内容一旦外泄就很难撤回。 / Key boundary: API keys, upload passwords, and admin credentials should stay in the server or environment files, not the frontend, screenshots, or public logs because once leaked they are hard to recover.
- 职责分离：前端负责展示，后端负责认证和转发，存储层负责持久化，隧道负责转发；把职责分开之后，审计和排障都会比“一个脚本包打一切”更清楚。 / Separation of duties: the frontend handles presentation, the backend handles authentication and forwarding, the storage layer handles persistence, and the tunnel handles transport; once separated, auditing and troubleshooting are much clearer than “one script does everything.”
- 文件安全：云盘目录里如果要放敏感文件，至少要确保上传路径、下载路径和目录遍历都只在受控权限下运行；不要假设“只有自己会访问”就可以省掉权限控制。 / File safety: if sensitive files live in the cloud drive, make sure upload, download, and directory traversal all run under controlled permissions; never assume “only I will use it” and skip access control.
- 文档安全：README 中可以公开地址、端口和使用方式，但不要公开密钥、内部 token 或私有备份路径；如果某条信息可能被他人直接利用，就应该留在私有配置里。 / Doc safety: the README can disclose public URLs, ports, and usage, but not secrets, internal tokens, or private backup paths; if a piece of information can be directly abused, keep it in private config.
- 日志边界：在分享日志时，先脱敏再贴出，尤其是 URL 参数、授权头、路径和文件名；排障需要可见性，但不需要把所有敏感上下文都公开出来。 / Log boundaries: when sharing logs, redact first, especially URL parameters, authorization headers, paths, and file names; debugging needs visibility, but it does not need all sensitive context exposed.
- 备份边界：备份时把源代码、配置和数据分开保存，这样恢复时可以按优先级逐层恢复，也更容易知道到底是哪一层出了问题。 / Backup boundaries: back up source, config, and data separately so recovery can happen in priority layers and it is easier to tell which layer failed.
- 配置边界：如果某项配置只对本机有效，就不要把它写成全局默认；本地实验配置和正式发布配置最好分开，避免测试值跑到线上。 / Config boundaries: if a setting only applies locally, do not turn it into a global default; keep experiment configs and production configs separate so test values do not leak into live deployments.
- 访问边界：如果以后引入用户管理或多角色访问，先定义谁能看、谁能传、谁能删，再定义 UI 入口；权限模型不清晰时，UI 只会把问题放大。 / Access boundaries: if user management or multi-role access is added later, define who can view, upload, or delete before designing the UI; when the permission model is unclear, the UI only amplifies the problem.
- 发布边界：GitHub Pages 和 Cloudflare Tunnel 都是公开面，任何一次发布都应默认“公开可见”，因此在推送之前先做一次内容审查，确认没有把临时信息、测试地址或敏感字段带上。 / Publish boundaries: GitHub Pages and Cloudflare Tunnel are public surfaces, so every publish should be treated as publicly visible by default; review content before pushing to ensure temporary info, test URLs, or sensitive fields are not included.
- 变更边界：如果改动可能影响外部访问方式，就先更新 README，再更新服务文件，最后再更新截图或示例；这样顺序最能减少用户看到“说明和实际不一致”的时间窗口。 / Change boundaries: if a change may affect how external access works, update the README first, service files second, and screenshots or examples last; this order minimizes the window where docs and reality diverge.
- 审查边界：代码审查时重点看是否把本应留在后端的东西暴露到了前端，或者把本应公开的东西错误地藏得太深；这两类问题都会直接影响维护成本。 / Review boundaries: in code review, focus on whether backend-only material was exposed to the frontend or whether public information was hidden too deeply; both problems directly increase maintenance cost.
- 责任边界：这份 README 负责让读者知道系统是什么、在哪、怎么用、怎么维护；更深入的模块逻辑、类设计和路由实现应该留在代码和子项目文档里。 / Responsibility boundary: this README should tell readers what the system is, where it lives, how to use it, and how to maintain it; deeper module logic, class design, and routing should live in code and subproject docs.

## 附录 H | Command Reference

| 命令 | 作用 | 说明 |
|------|------|------|
| `git status -sb` | 查看工作区状态 / Check working tree state | 先看有没有未提交改动，再决定要不要继续编辑。 / Check for pending changes before editing further. |
| `git log --oneline -n 3 -- README.md` | 查看 README 最近提交 / Review recent README commits | 快速判断当前文档是怎么演变到现在的。 / Quickly understand how the document evolved. |
| `git show --stat HEAD` | 查看最新提交摘要 / Inspect latest commit summary | 适合确认一次文档改动到底覆盖了哪些内容。 / Good for seeing what the latest edit actually changed. |
| `docker ps` | 查看容器状态 / List containers | 能快速判断 LobeChat 是否已经跑起来。 / Quickly shows whether LobeChat is up. |
| `systemctl status <service>` | 查看服务状态 / Check service status | 用于确认 cloud drive 或 cloudflared 是否正常守护。 / Confirm whether cloud drive or cloudflared is being supervised correctly. |
| `journalctl -u <service> -f` | 实时看日志 / Follow logs live | 适合盯住服务启动、重启和异常退出过程。 / Useful for watching startup, restart, and crash behavior. |
| `mkdocs build` | 构建文档站点 / Build docs site | 发布前先生成静态站点，确保导航和页面没有坏掉。 / Build the static site before publishing to ensure nav and pages are healthy. |
| `mkdocs serve` | 本地预览文档 / Preview docs locally | 适合在推送前检查页面布局、链接和表格。 / Great for checking layout, links, and tables before push. |
| `python -m venv .venv` | 创建 Python 虚拟环境 / Create Python venv | 用于隔离 cloud drive 服务依赖。 / Isolates cloud drive dependencies. |
| `pip install -r requirements.txt` | 安装 Python 依赖 / Install Python deps | 让云盘服务在一致的依赖集上运行。 / Ensures the cloud drive runs with a known dependency set. |
| `cloudflared tunnel run` | 启动隧道 / Start tunnel | 把本地服务转为公网入口。 / Turns local services into public endpoints. |
| `systemctl restart <service>` | 重启服务 / Restart service | 修改配置后最常见的生效动作。 / The usual way to apply config changes. |

## 附录 I | File Notes

| 文件/目录 | 作用 | 维护建议 |
|----------|------|----------|
| `README.md` | 根目录总入口 / Root landing page | 保持面向用户，优先说明全局结构和访问路径。 / Keep it user-facing and focus on global structure and access paths. |
| `my-project/README.md` | 子项目说明 / Subproject notes | 放实现和部署细节，适合更深入的排障信息。 / Use it for implementation and deployment details, including deeper troubleshooting. |
| `my-project/cloud_drive_server.py` | 云盘服务入口 / Cloud drive entrypoint | 改动前先确认端口、路径和权限是否一致。 / Check ports, paths, and permissions before editing. |
| `my-project/cloud-drive.service` | systemd 服务单元 / systemd unit | 修改后记得重载 systemd，再看启动日志。 / Reload systemd after edits, then review startup logs. |
| `my-project/cloud_gateway.py` | 云盘网关 / Cloud drive gateway | 同一公网入口按路径拆到 AI 和云盘。 / Splits one public endpoint to AI and cloud drive by path. |
| `my-project/cloud-gateway.service` | 网关服务单元 / Gateway unit | 先起网关，再让 Cloudflare Tunnel 指向它。 / Start the gateway first, then point Cloudflare Tunnel at it. |
| `my-project/cloudflared.service` | 隧道服务单元 / Tunnel unit | 把网关暴露到公网。 / Expose the gateway to the public Internet. |
| `my-project/mkdocs.yml` | 文档构建配置 / MkDocs config | 这里决定导航、主题和发布结构，改动要谨慎。 / It controls nav, theme, and publish structure, so edit carefully. |
| `my-project/docs/` | 文档源文件 / Docs source | 只改这里，不要把生成产物当源文件维护。 / Edit only here; do not maintain generated output as source. |
| `my-project/docs/stylesheets/extra.css` | 自定义样式 / Custom styles | 小范围改样式优先从这里下手，再看主题效果。 / Start here for scoped style changes and then verify theme behavior. |
| `my-project/site/` | 生成站点 / Generated site | 通常由构建产物覆盖，不建议手工编辑。 / Usually overwritten by builds and not meant for manual edits. |
| `my-project/requirements.txt` | Python 依赖 / Python requirements | 依赖更新后要重新验证服务启动和页面功能。 / Re-verify startup and page behavior after dependency updates. |
| `my-project/README.md` | 详细说明 / Detailed doc | 如果根目录 README 只想保留总览，这里放更具体的操作说明。 / Use this for deeper operational notes when the root README stays high-level. |

## 版本说明 | Version Notes

这份 README 的重点是把项目整体结构、在线入口、核心功能和维护方式讲清楚，方便后续持续更新。
The purpose of this README is to explain the overall structure, live entrypoints, core features, and maintenance approach clearly so future updates stay manageable.
