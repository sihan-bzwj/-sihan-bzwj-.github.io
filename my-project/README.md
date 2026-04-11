# my-project | 实现与部署说明

> 这个目录保存项目的实际服务代码、部署文件和文档站点源内容。  
> This directory contains the actual service code, deployment files, and documentation source for the project.

## 目录职责 | What Lives Here

- `cloud_drive_server.py`：云盘服务入口。  
  Cloud drive service entrypoint.
- `cloud_gateway.py`：统一网关入口。  
  Unified gateway entrypoint.
- `cloud_drive_app/`：云盘服务的配置、路径处理、上传解析、业务逻辑。  
  Config, path handling, upload parsing, and business logic for the cloud drive service.
- `cloud_gateway_app/`：网关配置、代理转发、静态站点服务、访客计数。  
  Gateway config, proxying, static site serving, and visitor counting.
- `docker-compose.lobechat.yml`：LobeChat 容器编排文件。  
  Docker Compose file for the LobeChat container.
- `lobe-chat.service`：LobeChat 的 `systemd` 单元。  
  `systemd` unit for LobeChat.
- `cloud-gateway.service`：网关的 `systemd` 单元。  
  `systemd` unit for the gateway.
- `cloud-drive.service`：云盘的 `systemd` 单元。  
  `systemd` unit for the cloud drive.
- `cloudflared.service`：Cloudflare Tunnel 的 `systemd` 单元。  
  `systemd` unit for Cloudflare Tunnel.
- `.env.lobechat.example`：LobeChat 环境变量模板。  
  Environment template for LobeChat.
- `docs/`：MkDocs 文档源文件。  
  MkDocs source files.
- `tests/`：标准库单元测试。  
  Standard-library unit tests.

## 当前部署方式 | Current Deployment Model

服务器上的实际组合如下：  
The live server currently uses the following combination:

```text
cloudflared.service
  -> cloud-gateway.service
     -> AI requests        -> LobeChat container on 127.0.0.1:3210
     -> /cloud-drive       -> cloud_drive_server.py on 127.0.0.1:8787
     -> local static site  -> /home/azureuser/site
```

这意味着：  
This means:

- 网关是唯一对外暴露的本地 HTTP 服务。  
  The gateway is the only local HTTP service exposed publicly.
- LobeChat 和云盘都应该只监听本机回环地址。  
  Both LobeChat and the cloud drive should listen only on the loopback interface.
- Cloudflare Tunnel 不直接连到 AI 容器，而是连到网关。  
  Cloudflare Tunnel connects to the gateway, not directly to the AI container.

## 服务器上已验证的运行状态 | Server-Verified Runtime State

以下状态基于 `2026-04-11` 的实际服务器检查：  
The following status is based on the actual server check performed on `2026-04-11`.

- `lobe-chat.service`：`active`  
  `lobe-chat.service`: `active`
- `cloud-gateway.service`：`active`  
  `cloud-gateway.service`: `active`
- `cloudflared.service`：`active`  
  `cloudflared.service`: `active`
- `http://127.0.0.1:3210/chat`：`200 OK`  
  `http://127.0.0.1:3210/chat`: `200 OK`
- `http://127.0.0.1:8080/chat`：`200 OK`  
  `http://127.0.0.1:8080/chat`: `200 OK`
- `https://procurement-trying-beside-beginning.trycloudflare.com/`：`200 OK`  
  `https://procurement-trying-beside-beginning.trycloudflare.com/`: `200 OK`

## 核心原理 | Core Principles

### 1. 网关优先 | Gateway-First Exposure

所有公网流量先到网关，再由网关根据路径分发。  
All public traffic lands on the gateway first, and the gateway dispatches requests by path.

这样做的原因：  
Why this matters:

- 统一入口，便于排障。  
  A single entrypoint makes troubleshooting simpler.
- AI、云盘、静态站点共享一个隧道。  
  AI, drive, and static content share a single tunnel.
- 服务可以继续保持本地监听，减少额外暴露。  
  Services can keep local-only listeners and reduce direct exposure.

### 2. systemd 管服务，Docker 管容器 | systemd Manages Services, Docker Manages Containers

- `systemd` 负责启动顺序、开机自启和日志。  
  `systemd` handles boot order, auto-start, and logs.
- Docker 负责 LobeChat 容器生命周期。  
  Docker handles the LobeChat container lifecycle.
- 网关和云盘由 Python 进程直接托管。  
  The gateway and cloud drive are hosted directly as Python processes.

### 3. 文档和运行配置分层 | Docs and Runtime Config Stay Separate

- README 记录真实运行状态和运维说明。  
  The README records the real runtime state and operational notes.
- `docs/` 负责面向访客的站点内容。  
  `docs/` is for visitor-facing site content.
- 服务器上的环境文件和 `systemd` 单元负责实际运行。  
  Server-side environment files and `systemd` units control the actual runtime.

## 技术栈 | Tech Stack

| 组件 Component | 技术 Technology | 说明 Notes |
|---|---|---|
| AI 平台 AI platform | LobeChat + Docker | 容器镜像为 `lobehub/lobe-chat:latest`。 / Container image is `lobehub/lobe-chat:latest`. |
| 网关 Gateway | Python stdlib HTTP server | 自定义反向代理、静态托管和访客统计。 / Custom reverse proxy, static serving, and visitor counting. |
| 云盘 Drive | Python stdlib HTTP server | 目录浏览、上传、下载、删除。 / Directory browsing, upload, download, and deletion. |
| 隧道 Tunnel | cloudflared | 把本地 `8080` 暴露为公网地址。 / Exposes local `8080` as a public URL. |
| 文档 Docs | MkDocs + GitHub Pages | 文档站点与项目说明页。 / Documentation site and project landing page. |
| 服务管理 Service manager | systemd | 保证服务顺序与长期运行。 / Keeps services ordered and running. |

## 常用命令 | Common Commands

### 本地开发 / 仓库侧 | Local Repo Side

```bash
python cloud_drive_server.py --host 127.0.0.1 --port 8787
python cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s tests
```

### 云服务器侧 | On the Server

```bash
sudo systemctl status lobe-chat.service --no-pager
sudo systemctl status cloud-gateway.service --no-pager
sudo systemctl status cloudflared.service --no-pager
docker ps -a
curl -I http://127.0.0.1:3210/chat
curl -I http://127.0.0.1:8080/chat
```

### 更新 systemd 文件 | Updating systemd Units

```bash
sudo cp /home/azureuser/<service>.service /etc/systemd/system/<service>.service
sudo systemctl daemon-reload
sudo systemctl restart <service>.service
```

## 最近的服务器修正 | Recent Server-Side Fixes

### 2026-04-11

- 把服务器上的 `cloud-gateway.service` 更新为仓库当前版本。  
  Updated the server-side `cloud-gateway.service` to the current repo version.
- 修复 `lobe-chat.service` 的容器名冲突，并改为 `docker compose up -d` 的托管模式。  
  Fixed the container-name conflict in `lobe-chat.service` and switched it to a `docker compose up -d` orchestration model.
- 使用现有 `lobe-chat.env` 衍生出 `.env.lobechat`，避免重复维护密钥。  
  Derived `.env.lobechat` from the existing `lobe-chat.env` to avoid duplicated secret management.

## 说明 | Notes

- 根目录 `README.md` 负责项目总览与线上状态。  
  The root `README.md` owns the project overview and live deployment state.
- 这里的 README 负责实现、部署与服务边界。  
  This README focuses on implementation, deployment, and service boundaries.
