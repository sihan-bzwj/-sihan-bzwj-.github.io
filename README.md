# Sihan's Blog | 思涵的个人网站
> 一个运行在 Azure 云服务器上的个人项目，集成 AI 对话平台、个人云盘和文档站点。  
> A personal project on an Azure VM that combines an AI chat platform, a personal cloud drive, and a documentation site.

![Status](https://img.shields.io/badge/Status-Migration%20In%20Progress-yellow)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Named-blue)

## 当前状态 | Current State

以下状态基于 `2026-04-11` 的本地仓库和服务器检查。  
The following state is based on the repo and server checks performed on `2026-04-11`.

| 项目 Item | 状态 Status | 说明 Notes |
|---|---|---|
| `lobe-chat.service` | `active` | AI 容器由 `systemd + docker compose` 托管。 |
| `cloud-gateway.service` | `active` | 网关已更新到仓库当前版本。 |
| `cloudflared.service` | `active` | 服务器已切到 Cloudflare dashboard 管理的 token tunnel。 |
| 本地 AI Local AI | `200 OK` | `http://127.0.0.1:3210/chat` |
| 本地网关 Local gateway | `200 OK` | `http://127.0.0.1:8080/chat` |
| GitHub Pages | `200 OK` | `https://sihan-bzwj.github.io/` |

当前不再把 Cloudflare Quick Tunnel 当正式入口。服务器已切到 Cloudflare dashboard 管理的 token tunnel，避免 Quick Tunnel 地址漂移。  
Quick Tunnel is no longer treated as the official entrypoint. The server now uses a dashboard-managed token tunnel to avoid Quick Tunnel URL drift.

## 目标入口 | Target Public Endpoints

| 服务 Service | 目标地址 Target URL | 说明 Description |
|---|---|---|
| AI 对话平台 AI chat | `https://ai.example.com/` | Named Tunnel 固定子域名。 / Fixed subdomain through Named Tunnel. |
| 云盘 Cloud drive | `https://drive.example.com/` | 独立固定子域名。 / Separate fixed subdomain. |
| 文档站点 Docs site | `https://sihan-bzwj.github.io/` | GitHub Pages 公开文档。 / Public docs on GitHub Pages. |

`ai.example.com` 和 `drive.example.com` 目前仍是占位符。运行层已经切到 token tunnel，但公开主机名仍需在 Cloudflare Zero Trust Dashboard 里绑定到真实域名。  
`ai.example.com` and `drive.example.com` are still placeholders. The runtime has been moved to a token tunnel, but public hostnames still need to be bound to a real domain in the Cloudflare Zero Trust Dashboard.

## 架构与原理 | Architecture and Principles

```text
Browser / Mobile Client
  -> Cloudflare Named Tunnel
    -> cloudflared.service
      -> cloud-gateway.service (127.0.0.1:8080)
         -> ai.example.com      -> LobeChat container (127.0.0.1:3210)
         -> drive.example.com   -> Python cloud drive service (127.0.0.1:8787)
         -> /                   -> local site content when needed
```

核心原则：
- 单一公网入口层：公网只暴露 `cloudflared`，业务服务仍绑定在 `127.0.0.1`。  
  Single public exposure layer: only `cloudflared` faces the internet while core services stay on `127.0.0.1`.
- 网关统一路由：AI、云盘和静态内容都先进入 Python 网关，再按主机名或路径分发。  
  Gateway-first routing: AI, drive, and static content all hit the Python gateway first and are then dispatched by host or path.
- 服务边界清晰：AI、网关、云盘、隧道分别由独立进程或容器承载，便于排障。  
  Clear service boundaries: AI, gateway, drive, and tunnel run as separate units for easier troubleshooting.
- 固定域名优先：dashboard 管理的 tunnel 比 Quick Tunnel 更适合作为正式入口，因为地址稳定，可持久绑定 DNS。  
  Fixed hostnames first: a dashboard-managed tunnel is a better production entrypoint than Quick Tunnel because it supports stable DNS binding.

## 技术栈 | Tech Stack

| 层级 Layer | 技术 Technology | 当前状态 / 版本 State / Version | 用途 Purpose |
|---|---|---|---|
| 操作系统 OS | Ubuntu | `22.04.5 LTS` | 云服务器运行环境。 / VM runtime environment. |
| AI 平台 AI platform | LobeChat | `lobehub/lobe-chat:latest` | 提供统一 AI 对话入口。 / Unified AI chat interface. |
| 网关 Gateway | Python 3 | `3.10.12` | 反向代理、静态托管、访客统计。 / Reverse proxy, static serving, visitor counting. |
| 云盘 Drive | Python stdlib HTTP service | custom | 文件浏览、上传、下载、删除。 / File browsing, upload, download, deletion. |
| 容器运行时 Container runtime | Docker | `29.3.1` | 托管 LobeChat 容器。 / Hosts the LobeChat container. |
| 公网隧道 Public tunnel | cloudflared | `2026.3.0` | 通过 Named Tunnel 绑定固定子域名。 / Binds fixed subdomains through a Named Tunnel. |
| 服务管理 Service manager | systemd | Ubuntu native | 管理开机自启、重启和日志。 / Manages startup, restart, and logs. |
| 文档站点 Docs | MkDocs + GitHub Pages | repo-managed | 构建并发布公开文档。 / Builds and publishes public docs. |

## 仓库重点文件 | Key Repo Files

- `my-project/cloudflared.service`：token 管理模式的 Cloudflare Tunnel `systemd` 单元。  
  `systemd` unit for the token-managed Cloudflare Tunnel.
- `my-project/cloudflared.quick-tunnel.service`：旧 Quick Tunnel 兼容参考。  
  Legacy Quick Tunnel unit kept for reference.
- `my-project/cloudflared-config.example.yml`：本地管理 tunnel 的可选参考模板。  
  Optional reference template for locally managed tunnels.
- `my-project/cloud-gateway.service`：统一网关服务。  
  Unified gateway service.
- `my-project/lobe-chat.service`：LobeChat 容器托管服务。  
  Service that manages the LobeChat container.
- `my-project/docker-compose.lobechat.yml`：LobeChat 的 Docker Compose 配置。  
  Docker Compose file for LobeChat.

## 服务器切换步骤 | Server Cutover Steps

1. 在 Cloudflare Zero Trust Dashboard 创建 tunnel。  
   Create a tunnel in the Cloudflare Zero Trust Dashboard.
2. 在 tunnel 页面复制 `cloudflared service install ...` 里的 token。  
   Copy the token from the `cloudflared service install ...` command shown in the tunnel page.
3. 在服务器写入 `/home/azureuser/.cloudflared/cloudflared-token.env`：  
   Write `/home/azureuser/.cloudflared/cloudflared-token.env` on the server:
   `TUNNEL_TOKEN=...`
4. 用仓库里的 `my-project/cloudflared.service` 覆盖服务器上的 `/etc/systemd/system/cloudflared.service`，然后 `daemon-reload` 并重启服务。  
   Replace `/etc/systemd/system/cloudflared.service` on the server with `my-project/cloudflared.service`, then run `daemon-reload` and restart the service.
5. 在 Dashboard 里为 tunnel 绑定 `ai.<your-domain>` 和 `drive.<your-domain>` 这两个 public hostnames。  
   Bind `ai.<your-domain>` and `drive.<your-domain>` as public hostnames for the tunnel in the Dashboard.

## 常用排查 | Troubleshooting

```bash
sudo systemctl status lobe-chat.service --no-pager
sudo systemctl status cloud-gateway.service --no-pager
sudo systemctl status cloudflared.service --no-pager
docker ps -a
curl -I http://127.0.0.1:3210/chat
curl -I http://127.0.0.1:8080/chat
ls -la ~/.cloudflared
sudo cat /etc/systemd/system/cloudflared.service
```

- 如果 AI 页面打不开，但本地 `127.0.0.1:3210` 和 `127.0.0.1:8080` 正常，优先检查 `cloudflared.service` 是否载入了正确的 `TUNNEL_TOKEN`，以及 Dashboard 里的 public hostname 是否指向当前 tunnel。  
  If the AI page is down while local `127.0.0.1:3210` and `127.0.0.1:8080` are healthy, first check whether `cloudflared.service` loaded the correct `TUNNEL_TOKEN` and whether the Dashboard public hostname points to the current tunnel.

## 更新记录 | Update Log

### 2026-04-11

- 已把服务器上的 `cloud-gateway.service` 更新到仓库当前版本。  
  Updated the server-side `cloud-gateway.service` to the current repo version.
- 已修复 `lobe-chat.service` 的容器名冲突，并改为 `docker compose up -d` 托管方式。  
  Fixed the `lobe-chat.service` container-name conflict and switched it to `docker compose up -d`.
- 已把服务器切到 dashboard 管理的 token tunnel，并同步更新仓库中的 `cloudflared.service` 说明。  
  Switched the server to a dashboard-managed token tunnel and updated the repository `cloudflared.service` accordingly.
