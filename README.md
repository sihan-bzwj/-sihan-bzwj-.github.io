# Sihan's Blog | 思涵的个人网站

> 一个运行在 Azure 云服务器上的个人项目，把 AI 对话平台、个人云盘和静态文档站点整合到同一套基础设施中。  
> A personal project running on an Azure VM that combines an AI chat platform, a personal cloud drive, and a static documentation site on one infrastructure stack.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick-orange)

## 当前状态 | Live Status

以下状态已于 `2026-04-11` 实际核对。  
The following status was verified on `2026-04-11`.

| 项目 Item | 当前状态 Current State | 说明 Notes |
|---|---|---|
| AI 对话平台 AI chat | `200 OK` | 公网 `https://procurement-trying-beside-beginning.trycloudflare.com/` 可访问。 |
| 云盘 Cloud drive | `200 OK` | 公网 `https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive` 可访问。 |
| GitHub Pages | `200 OK` | `https://sihan-bzwj.github.io/` 从服务器侧验证可访问。 |
| `lobe-chat.service` | `active` | 通过 `systemd + docker compose` 管理。 |
| `cloud-gateway.service` | `active` | 已同步到仓库当前版本。 |
| `cloudflared.service` | `active` | 正在把本地 `8080` 暴露到公网。 |
| AI 本地入口 Local AI | `200 OK` | `http://127.0.0.1:3210/chat` 正常。 |
| 网关本地入口 Local gateway | `200 OK` | `http://127.0.0.1:8080/chat` 正常。 |

> 当前 Cloudflare Quick Tunnel 地址是 `https://procurement-trying-beside-beginning.trycloudflare.com`。  
> The current Cloudflare Quick Tunnel URL is `https://procurement-trying-beside-beginning.trycloudflare.com`.
>
> Quick Tunnel 地址在 `cloudflared` 重启或隧道重建后可能变化。  
> The Quick Tunnel URL may change after `cloudflared` restarts or the tunnel is recreated.

## 在线入口 | Live Access

| 服务 Service | 地址 URL | 说明 Description |
|---|---|---|
| AI 对话平台 AI chat | https://procurement-trying-beside-beginning.trycloudflare.com/ | LobeChat 主入口。 / Main LobeChat entrypoint. |
| 云盘 Cloud drive | https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive | 文件浏览、上传、下载、建目录、删除。 / Browse, upload, download, create folders, and delete entries. |
| 项目主页 Project home | https://sihan-bzwj.github.io/ | GitHub Pages + MkDocs 静态站点。 / Static site powered by GitHub Pages and MkDocs. |
| 仓库 Repository | https://github.com/sihan-bzwj/sihan-bzwj.github.io | 源码、服务文件和文档。 / Source code, service files, and docs. |

## 项目概览 | Overview

这个仓库不是单独保存某一个应用，而是保存整套运行方案：  
This repository does not only store one application, but the whole operating setup:

- AI 对话平台：LobeChat 运行在 Docker 容器中，对外由 Python 网关和 Cloudflare Tunnel 暴露。  
  AI chat platform: LobeChat runs in a Docker container and is exposed through a Python gateway plus Cloudflare Tunnel.
- 个人云盘：一个基于 Python 的轻量 HTTP 文件服务，通过同一个网关挂载到 `/cloud-drive`。  
  Personal cloud drive: a lightweight Python HTTP file service mounted under `/cloud-drive` through the same gateway.
- 静态站点：MkDocs 构建的文档站点发布到 GitHub Pages，同时服务器网关也能托管本地 `site/` 内容。  
  Static site: an MkDocs-built documentation site published to GitHub Pages, while the server gateway can also serve local `site/` content.

## 功能说明 | Feature Summary

### AI 对话平台 | AI Chat Platform

- 使用 LobeChat 提供统一的多模型对话入口。  
  Uses LobeChat as the unified multi-model chat interface.
- 对外访问路径由 `cloud-gateway.service` 转发到本地 `127.0.0.1:3210`。  
  External traffic is forwarded by `cloud-gateway.service` to local `127.0.0.1:3210`.
- 模型密钥和访问控制保留在服务器环境文件中，而不是写在前端页面里。  
  Provider keys and access control stay in server-side environment files instead of frontend code.
- 常见供应商包括 OpenRouter、OpenAI、Anthropic、Google Gemini、Mistral、Groq、DeepSeek、Cohere 等。  
  Common providers include OpenRouter, OpenAI, Anthropic, Google Gemini, Mistral, Groq, DeepSeek, Cohere, and others.

### 云盘服务 | Cloud Drive

- 支持目录浏览、文件上传、文件下载、创建目录和删除文件或目录。  
  Supports directory browsing, file upload, file download, folder creation, and file or directory deletion.
- 上传和删除都依赖服务端密码。  
  Upload and delete operations are protected by a server-side password.
- 路径解析和下载路径都被限制在云盘根目录内部，避免路径逃逸。  
  Path resolution and download targets are constrained to the storage root to prevent traversal escapes.

### 站点与运维 | Site and Operations

- GitHub Pages 承载公开文档站点。  
  GitHub Pages hosts the public documentation site.
- 服务器上的 Python 网关也能托管本地 `site/` 目录。  
  The Python gateway on the server can also serve the local `site/` directory.
- `systemd` 负责管理 `lobe-chat`、`cloud-gateway`、`cloudflared` 等长期运行服务。  
  `systemd` manages long-running services such as `lobe-chat`, `cloud-gateway`, and `cloudflared`.

## 架构与原理 | Architecture and Principles

```text
Browser / Web Client
  -> Cloudflare Quick Tunnel
    -> cloudflared.service
      -> cloud-gateway.service (127.0.0.1:8080)
         -> /chat and /              -> LobeChat container (127.0.0.1:3210)
         -> /cloud-drive             -> Python cloud drive service (127.0.0.1:8787)
         -> /static content          -> /home/azureuser/site
```

### 请求路径 | Request Flow

AI 请求路径：  
AI request flow:

```text
User -> Cloudflare Tunnel -> Gateway :8080 -> LobeChat :3210 -> Model provider API -> Response stream
```

云盘请求路径：  
Cloud drive request flow:

```text
User -> Cloudflare Tunnel -> Gateway :8080/cloud-drive -> Python drive service :8787 -> Local storage root
```

### 设计原则 | Design Principles

- 单公网入口：AI、云盘和本地静态站点共用一个公网入口，减少暴露面。  
  Single public entrypoint: AI, drive, and local static content share one public entrypoint to reduce exposed surface area.
- 本地回环绑定：核心服务绑定到 `127.0.0.1`，只通过网关对外暴露。  
  Loopback binding: core services bind to `127.0.0.1` and are exposed only through the gateway.
- 服务分层：AI 平台、网关、云盘、隧道分别独立，定位问题时边界清晰。  
  Layered services: AI platform, gateway, drive, and tunnel are independent, which keeps troubleshooting boundaries clear.
- 文档与运行配置分离：文档站点在仓库里维护，服务器运行文件由 `systemd` 和 Docker 管理。  
  Separation of docs and runtime config: documentation stays in the repo, while server runtime is managed by `systemd` and Docker.

## 技术栈 | Tech Stack

下面的版本以 `2026-04-11` 在服务器上实际检查到的结果为准。  
The versions below reflect what was actually checked on the server on `2026-04-11`.

| 层级 Layer | 技术 Technology | 当前状态 / 版本 Current State / Version | 用途 Purpose |
|---|---|---|---|
| 操作系统 OS | Ubuntu | `22.04.5 LTS` | 云服务器基础运行环境。 / Base runtime environment on the VM. |
| AI 平台 AI platform | LobeChat | `lobehub/lobe-chat:latest` 容器镜像 / container image | AI 对话前后端。 / AI chat frontend and backend. |
| 网关 Gateway | Python | `Python 3.10.12` | 路由 AI、云盘和本地站点。 / Routes AI, drive, and local site content. |
| 云盘后端 Cloud drive backend | Python stdlib HTTP service | 自定义实现 / custom implementation | 文件目录浏览与上传下载。 / File browsing plus upload/download. |
| 容器运行时 Container runtime | Docker | `29.3.1` | 运行 LobeChat 容器。 / Runs the LobeChat container. |
| 公网隧道 Public tunnel | cloudflared | `2026.3.0` | 将本地 `8080` 暴露到公网。 / Exposes local `8080` to the public internet. |
| 服务管理 Service manager | systemd | Ubuntu native | 管理长期运行服务。 / Manages long-running services. |
| 文档站点 Docs site | MkDocs + GitHub Pages | 仓库配置 / repo-managed | 构建并发布项目文档。 / Builds and publishes project docs. |

## 当前服务器部署 | Current Server Deployment

服务器路径与职责：  
Key server paths and responsibilities:

- `/home/azureuser/bin/cloud_gateway.py`：网关入口脚本。  
  Gateway entry script.
- `/home/azureuser/bin/cloud_drive_server.py`：云盘服务脚本。  
  Cloud drive service script.
- `/home/azureuser/site`：本地静态站点目录。  
  Local static site directory.
- `/home/azureuser/cloud-drive`：云盘根目录。  
  Cloud drive storage root.
- `/home/azureuser/.env.lobechat`：LobeChat 环境配置。  
  LobeChat environment configuration.
- `/etc/systemd/system/lobe-chat.service`：AI 平台 systemd 单元。  
  AI platform systemd unit.
- `/etc/systemd/system/cloud-gateway.service`：网关 systemd 单元。  
  Gateway systemd unit.
- `/etc/systemd/system/cloudflared.service`：隧道 systemd 单元。  
  Tunnel systemd unit.

## 仓库结构 | Repository Layout

```text
.
├─ README.md
└─ my-project/
   ├─ README.md
   ├─ cloud_drive_server.py
   ├─ cloud_gateway.py
   ├─ cloud_drive_app/
   ├─ cloud_gateway_app/
   ├─ docs/
   ├─ tests/
   ├─ cloud-drive.service
   ├─ cloud-gateway.service
   ├─ cloudflared.service
   ├─ docker-compose.lobechat.yml
   ├─ lobe-chat.service
   ├─ .env.lobechat.example
   └─ mkdocs.yml
```

## 运行与排查 | Runbook and Troubleshooting

### 常用命令 | Common Commands

```bash
sudo systemctl status lobe-chat.service --no-pager
sudo systemctl status cloud-gateway.service --no-pager
sudo systemctl status cloudflared.service --no-pager
docker ps -a
curl -I http://127.0.0.1:3210/chat
curl -I http://127.0.0.1:8080/chat
curl -L -s -o /dev/null -w '%{http_code}' https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive
```

### 常见问题 | Common Issues

- AI 页面打不开，但服务器容器还在跑：先看 `cloud-gateway.service` 是否仍指向 `127.0.0.1:3210`，再看隧道地址是否变化。  
  If the AI page is unavailable while the container is still running, first check whether `cloud-gateway.service` still points to `127.0.0.1:3210`, then verify whether the tunnel URL changed.
- README 地址失效：Quick Tunnel 地址不是固定域名，重启 `cloudflared` 后需要同步文档。  
  If README links go stale, remember that Quick Tunnel URLs are not fixed domains and must be updated after `cloudflared` restarts.
- 云盘上传失败：优先检查上传密码、目录权限和 `cloud-drive.service` 日志。  
  For upload failures, first check the upload password, directory permissions, and `cloud-drive.service` logs.

## 更新记录 | Update Log

### 2026-04-11

- 已把服务器上的 `cloud-gateway.service` 更新到仓库当前版本，包含 `lobe-chat.service` 依赖和 `--site-dir /home/azureuser/site`。  
  Updated the server-side `cloud-gateway.service` to the current repo version, including the `lobe-chat.service` dependency and `--site-dir /home/azureuser/site`.
- 已修复 `lobe-chat.service` 的容器名冲突问题，并将其改为更适合 `docker compose up -d` 的方式。  
  Fixed the `lobe-chat.service` container-name conflict and changed it to a model better suited for `docker compose up -d`.
- 已重新整理 README，恢复更完整的项目说明，并补充原理、技术栈、部署结构与双语说明。  
  Reworked the README, restored fuller project documentation, and added architecture, tech stack, deployment structure, and bilingual explanations.

## 备注 | Notes

- 这个 README 记录的是项目总览与当前线上状态。  
  This README is the project-level overview plus the current live deployment state.
- `my-project/README.md` 记录实现、服务文件和部署细节。  
  `my-project/README.md` records implementation details, service files, and deployment notes.
