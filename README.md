# Sihan's Blog | 思涵的个人网站
> 一个运行在 Azure 云服务器上的个人项目，当前公开内容以个人云盘和文档站点为主。  
> A personal project on an Azure VM, now focused publicly on the cloud drive and documentation site.

![Status](https://img.shields.io/badge/Status-Public%20AI%20Entry%20Removed-lightgrey)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Python-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Token%20Tunnel-blue)

## 当前状态 | Current State

以下状态基于 `2026-04-11` 的本地仓库和服务器检查。  
The following state is based on the repo and server checks performed on `2026-04-11`.

| 项目 Item | 状态 Status | 说明 Notes |
|---|---|---|
| `cloud-gateway.service` | `active` | 网关已更新到仓库当前版本。 / The gateway is on the current repo version. |
| `cloudflared.service` | `active` | 服务器已切到 Cloudflare dashboard 管理的 token tunnel。 / The server now uses a dashboard-managed token tunnel. |
| `lobe-chat.service` | `stopped` | 已停止并禁用。 / Stopped and disabled. |
| GitHub Pages | `200 OK` | `https://sihan-bzwj.github.io/` |
| AI 公网入口 Public AI entry | `removed` | 文档、首页和导航中不再公开 AI 访问入口。 / The AI entry is no longer exposed in docs, homepage, or navigation. |

## 公开入口 | Public Endpoints

| 服务 Service | 地址 URL | 说明 Description |
|---|---|---|
| 云盘 Cloud drive | `https://drive.example.com/` | 仅保留云盘的未来固定域名占位。 / Placeholder for a future fixed cloud-drive hostname only. |
| 文档站点 Docs site | `https://sihan-bzwj.github.io/` | GitHub Pages 公开文档。 / Public docs on GitHub Pages. |

`drive.example.com` 仍是占位符。当前没有托管到 Cloudflare 的真实域名，因此固定公网域名尚未绑定。  
`drive.example.com` is still a placeholder. No real domain is currently managed in Cloudflare, so a fixed public hostname has not been bound yet.

## AI 删除原因记录 | AI Removal Record

`2026-04-11` 起，仓库和公开文档不再保留 AI 公网入口，服务器上的 `lobe-chat.service` 和容器也已停止。  
Starting on `2026-04-11`, the repository and public docs no longer keep a public AI entry, and the server-side `lobe-chat.service` plus container have also been stopped.

删除原因：
- 当前没有接入 Cloudflare 的真实域名，无法给 AI 服务绑定稳定、可持续的固定主机名。  
  There is no real domain managed in Cloudflare yet, so the AI service cannot be bound to a stable long-term hostname.
- Quick Tunnel 只适合临时测试，不适合作为 README、文档和手机访问使用的正式入口。  
  Quick Tunnel is suitable only for temporary testing, not as an official entrypoint for the README, public docs, or mobile access.
- 继续保留 AI 公网入口会制造失效链接，因此改为彻底下线服务并仅保留原因记录。  
  Keeping the public AI entry would create broken links, so the service was fully taken offline and only the removal record was kept.

当前处理结果：
- AI 公网入口已删除
- `lobe-chat.service` 已停止并禁用
- 公开文档只保留云盘和项目文档入口

Current handling:
- The public AI entry has been removed
- `lobe-chat.service` has been stopped and disabled
- Public docs now keep only the cloud-drive and project-doc entrypoints

## 架构与原理 | Architecture and Principles

```text
Public browser
  -> GitHub Pages docs
  -> Cloudflare tunnel (future drive-only public exposure)
    -> cloud-gateway.service (127.0.0.1:8080)
       -> /cloud-drive          -> Python cloud drive service (127.0.0.1:8787)
```

核心原则：
- 删除无效入口：已经不再对外提供的服务，不继续保留公开链接或入口说明。  
  Remove dead entrypoints: if a service is no longer public, its public links and entry descriptions should not remain.
- 网关统一承接：当前只保留云盘相关的公网流量入口。  
  Unified gateway: only drive-related public traffic remains.
- 固定域名优先：在没有真实域名之前，不再假装存在稳定公网地址。  
  Fixed domains first: without a real domain, the project should not pretend a stable public URL exists.
- 文档与真实状态一致：README 和站点只保留当前可持续维护的公开入口。  
  Docs must match reality: README and the site keep only the public entrypoints that can actually be maintained.

## 技术栈 | Tech Stack

| 层级 Layer | 技术 Technology | 当前状态 / 版本 State / Version | 用途 Purpose |
|---|---|---|---|
| 操作系统 OS | Ubuntu | `22.04.5 LTS` | 云服务器运行环境。 / VM runtime environment. |
| 网关 Gateway | Python 3 | `3.10.12` | 反向代理、静态托管、访客统计。 / Reverse proxy, static serving, visitor counting. |
| 云盘 Drive | Python stdlib HTTP service | custom | 文件浏览、上传、下载、删除。 / File browsing, upload, download, deletion. |
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

## 常用排查 | Troubleshooting

```bash
sudo systemctl status cloud-gateway.service --no-pager
sudo systemctl status cloudflared.service --no-pager
sudo systemctl status lobe-chat.service --no-pager
docker ps -a
ls -la ~/.cloudflared
sudo cat /etc/systemd/system/cloudflared.service
```

- 如果未来要恢复公网入口，应先获得真实域名，再重新评估是否恢复云盘或其他服务的公网主机名。  
  If public entrypoints are restored in the future, acquire a real domain first and then re-evaluate whether drive or other services should return.

## 更新记录 | Update Log

### 2026-04-11

- 已把服务器上的 `cloud-gateway.service` 更新到仓库当前版本。  
  Updated the server-side `cloud-gateway.service` to the current repo version.
- 已把服务器切到 dashboard 管理的 token tunnel，并同步更新仓库中的 `cloudflared.service` 说明。  
  Switched the server to a dashboard-managed token tunnel and updated the repository `cloudflared.service` accordingly.
- 已移除公开 AI 入口，并记录移除原因。  
  Removed the public AI entry and recorded the removal reason.
- 已停止并禁用服务器上的 `lobe-chat.service`，同时移除容器。  
  Stopped and disabled `lobe-chat.service` on the server and removed the container.
