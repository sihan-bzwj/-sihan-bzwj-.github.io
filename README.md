# Sihan's Blog | 思涵的个人网站
> 一个运行在 Azure 云服务器上的个人项目，集成 AI 对话平台、个人云盘和文档站点。  
> A personal project on an Azure VM that combines an AI chat platform, a personal cloud drive, and documentation.

![Status](https://img.shields.io/badge/Status-Public%20AI%20Entry%20Removed-lightgrey)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Token%20Tunnel-blue)

## 当前状态 | Current State

以下状态基于 `2026-04-11` 的本地仓库和服务器检查。  
The following state is based on the repo and server checks performed on `2026-04-11`.

| 项目 Item | 状态 Status | 说明 Notes |
|---|---|---|
| `lobe-chat.service` | `active` | AI 容器仍在服务器本地运行。 / The AI container still runs locally on the server. |
| `cloud-gateway.service` | `active` | 网关已更新到仓库当前版本。 / The gateway is on the current repo version. |
| `cloudflared.service` | `active` | 服务器已切到 Cloudflare dashboard 管理的 token tunnel。 / The server now uses a dashboard-managed token tunnel. |
| 本地 AI Local AI | `200 OK` | `http://127.0.0.1:3210/chat` |
| 本地网关 Local gateway | `200 OK` | `http://127.0.0.1:8080/chat` |
| GitHub Pages | `200 OK` | `https://sihan-bzwj.github.io/` |
| AI 公网入口 Public AI entry | `removed` | 文档、首页和导航中不再公开 AI 访问入口。 / The AI entry is no longer exposed in docs, homepage, or navigation. |

## 公开入口 | Public Endpoints

| 服务 Service | 地址 URL | 说明 Description |
|---|---|---|
| 云盘 Cloud drive | `https://drive.example.com/` | 仅保留云盘的未来固定域名占位。 / Placeholder for a future fixed cloud-drive hostname only. |
| 文档站点 Docs site | `https://sihan-bzwj.github.io/` | GitHub Pages 公开文档。 / Public docs on GitHub Pages. |

`drive.example.com` 仍是占位符。当前没有托管到 Cloudflare 的真实域名，因此固定公网域名尚未绑定。  
`drive.example.com` is still a placeholder. No real domain is currently managed in Cloudflare, so a fixed public hostname has not been bound yet.

## AI 入口移除记录 | AI Entry Removal Record

`2026-04-11` 起，仓库和公开文档不再保留 AI 公网入口。AI 服务本身没有删除，只是不再作为公开站点的一部分暴露。  
Starting on `2026-04-11`, the repository and public docs no longer expose a public AI entry. The AI service itself has not been removed; it is simply no longer exposed as part of the public site.

移除原因：
- 当前没有接入 Cloudflare 的真实域名，无法给 AI 服务绑定稳定、可持续的固定主机名。  
  There is no real domain managed in Cloudflare yet, so the AI service cannot be bound to a stable long-term hostname.
- Quick Tunnel 只适合临时测试，不适合作为 README、文档和手机访问使用的正式入口。  
  Quick Tunnel is suitable only for temporary testing, not as an official entrypoint for the README, public docs, or mobile access.
- AI 服务对连接稳定性更敏感，继续保留一个不稳定的公开入口只会制造失效链接。  
  The AI service is more sensitive to connection stability, and keeping an unstable public entry would only create broken links.

当前处理结果：
- AI 仍保留在服务器本地：`127.0.0.1:3210`
- 网关仍可代理 AI：`127.0.0.1:8080/chat`
- 公开文档只保留云盘和项目文档入口

Current handling:
- AI remains available locally on the server: `127.0.0.1:3210`
- The gateway can still proxy AI locally: `127.0.0.1:8080/chat`
- Public docs now keep only the cloud-drive and project-doc entrypoints

## 架构与原理 | Architecture and Principles

```text
Public browser
  -> GitHub Pages docs
  -> Cloudflare tunnel (future drive-only public exposure)
    -> cloud-gateway.service (127.0.0.1:8080)
       -> /cloud-drive          -> Python cloud drive service (127.0.0.1:8787)

Local server access
  -> cloud-gateway.service (127.0.0.1:8080)
     -> /chat                  -> LobeChat container (127.0.0.1:3210)
```

核心原则：
- AI 保留、入口移除：保留运行能力，但不再对公开文档暴露不稳定入口。  
  Keep the AI runtime, remove the public entry: preserve the service while avoiding unstable public exposure.
- 网关统一承接：AI 和云盘都先进入 Python 网关，再按路径分发。  
  Unified gateway: both AI and drive traffic land on the Python gateway first and are dispatched by path.
- 固定域名优先：在没有真实域名之前，不再假装存在稳定 AI 公网地址。  
  Fixed domains first: without a real domain, the project should not pretend a stable public AI URL exists.
- 文档与真实状态一致：README 和站点只保留当前可持续维护的公开入口。  
  Docs must match reality: README and the site keep only the public entrypoints that can actually be maintained.

## 技术栈 | Tech Stack

| 层级 Layer | 技术 Technology | 当前状态 / 版本 State / Version | 用途 Purpose |
|---|---|---|---|
| 操作系统 OS | Ubuntu | `22.04.5 LTS` | 云服务器运行环境。 / VM runtime environment. |
| AI 平台 AI platform | LobeChat | `lobehub/lobe-chat:latest` | 本地保留 AI 运行能力。 / Keeps local AI runtime capability. |
| 网关 Gateway | Python 3 | `3.10.12` | 反向代理、静态托管、访客统计。 / Reverse proxy, static serving, visitor counting. |
| 云盘 Drive | Python stdlib HTTP service | custom | 文件浏览、上传、下载、删除。 / File browsing, upload, download, deletion. |
| 容器运行时 Container runtime | Docker | `29.3.1` | 托管 LobeChat 容器。 / Hosts the LobeChat container. |
| 公网隧道 Public tunnel | cloudflared | `2026.3.0` | 保留为后续固定域名或云盘公网入口做准备。 / Kept for future fixed-hostname or drive-public exposure. |
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

- 如果只需要确认 AI 是否仍在服务器本地可用，优先检查 `127.0.0.1:3210/chat` 和 `127.0.0.1:8080/chat`。  
  If you only need to confirm that AI is still locally available on the server, check `127.0.0.1:3210/chat` and `127.0.0.1:8080/chat` first.
- 如果未来要恢复公网入口，应先获得真实域名，再重新评估是否恢复云盘或 AI 的公网主机名。  
  If public entrypoints are restored in the future, acquire a real domain first and then re-evaluate whether drive or AI hostnames should return.

## 更新记录 | Update Log

### 2026-04-11

- 已把服务器上的 `cloud-gateway.service` 更新到仓库当前版本。  
  Updated the server-side `cloud-gateway.service` to the current repo version.
- 已修复 `lobe-chat.service` 的容器名冲突，并改为 `docker compose up -d` 托管方式。  
  Fixed the `lobe-chat.service` container-name conflict and switched it to `docker compose up -d`.
- 已把服务器切到 dashboard 管理的 token tunnel，并同步更新仓库中的 `cloudflared.service` 说明。  
  Switched the server to a dashboard-managed token tunnel and updated the repository `cloudflared.service` accordingly.
- 已移除公开 AI 入口，并记录移除原因；AI 服务仍保留在服务器本地运行。  
  Removed the public AI entry and recorded the reason; the AI service remains available locally on the server.
