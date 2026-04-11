# my-project | 实现与部署说明
> 这个目录保存项目的服务代码、部署文件和文档源码。  
> This directory contains the service code, deployment files, and documentation source.

## 目录职责 | What Lives Here

- `cloud_drive_app/`：云盘服务的配置、路径处理、上传解析和业务逻辑。  
  Config, path handling, upload parsing, and business logic for the drive service.
- `cloud_gateway_app/`：网关配置、反向代理、静态站点托管和访客统计。  
  Gateway config, reverse proxying, static-site serving, and visitor counting.
- `cloud_drive_server.py`：云盘服务入口。  
  Cloud drive entrypoint.
- `cloud_gateway.py`：统一网关入口。  
  Unified gateway entrypoint.
- `docker-compose.lobechat.yml`：LobeChat 的容器编排。  
  Docker Compose for LobeChat.
- `lobe-chat.service`：LobeChat 的 `systemd` 单元。  
  `systemd` unit for LobeChat.
- `cloud-gateway.service`：网关的 `systemd` 单元。  
  `systemd` unit for the gateway.
- `cloud-drive.service`：云盘的 `systemd` 单元。  
  `systemd` unit for the drive service.
- `cloudflared.service`：token 管理模式的 Cloudflare Tunnel `systemd` 单元。  
  `systemd` unit for the token-managed Cloudflare Tunnel.
- `cloudflared.quick-tunnel.service`：旧 Quick Tunnel 兼容参考。  
  Legacy Quick Tunnel unit kept for reference.
- `cloudflared-config.example.yml`：本地管理 tunnel 的可选参考模板。  
  Optional reference template for a locally managed tunnel.
- `docs/`：MkDocs 文档源文件。  
  MkDocs documentation source.
- `tests/`：标准库单元测试。  
  Standard-library unit tests.

## 当前部署模型 | Current Deployment Model

```text
cloudflared.service
  -> cloud-gateway.service
     -> ai.example.com      -> LobeChat container on 127.0.0.1:3210
     -> drive.example.com   -> cloud_drive_server.py on 127.0.0.1:8787
     -> local static site   -> /home/azureuser/site
```

要点：
- 网关是唯一对外暴露的本地 HTTP 服务。  
  The gateway is the only local HTTP service exposed outward.
- AI 和云盘都应该只监听本机回环地址。  
  AI and drive services should listen only on loopback.
- Named Tunnel 连接的是网关，不是 AI 容器本身。  
  The Named Tunnel connects to the gateway, not directly to the AI container.

## 服务器已确认的状态 | Server-Verified State

基于 `2026-04-11` 的服务器实际检查：  
Based on the actual server checks performed on `2026-04-11`:

- `lobe-chat.service`: `active`
- `cloud-gateway.service`: `active`
- `http://127.0.0.1:3210/chat`: `200 OK`
- `http://127.0.0.1:8080/chat`: `200 OK`
- `cloudflared.service`: `active`
- Cloudflare tunnel runtime: token managed

## 原理 | Principles

- 网关优先：所有外部流量先到 Python 网关，再转发给 AI、云盘或静态站点。  
  Gateway first: all external traffic reaches the Python gateway before being dispatched to AI, drive, or static content.
- 服务解耦：`systemd` 管启动顺序和日志，Docker 管 LobeChat 容器，Python 进程管网关和云盘。  
  Decoupled services: `systemd` handles startup order and logs, Docker handles the LobeChat container, and Python processes handle gateway and drive.
- 固定域名：dashboard 管理的 tunnel 提供稳定 DNS 入口，适合 README、文档和手机访问。  
  Fixed hostnames: a dashboard-managed tunnel provides stable DNS entrypoints suitable for docs, README links, and mobile access.

## 技术栈 | Tech Stack

| 组件 Component | 技术 Technology | 说明 Notes |
|---|---|---|
| AI 平台 AI platform | LobeChat + Docker | 容器镜像为 `lobehub/lobe-chat:latest`。 / Container image `lobehub/lobe-chat:latest`. |
| 网关 Gateway | Python stdlib HTTP server | 自定义反向代理、静态托管和访客统计。 / Custom reverse proxy, static serving, visitor counting. |
| 云盘 Drive | Python stdlib HTTP server | 目录浏览、上传、下载、删除。 / Directory browsing, upload, download, deletion. |
| 隧道 Tunnel | cloudflared | 通过 dashboard 管理的 tunnel 绑定固定子域名。 / Binds fixed subdomains through a dashboard-managed tunnel. |
| 文档 Docs | MkDocs + GitHub Pages | 文档站点与项目说明页。 / Docs site and project landing pages. |
| 服务管理 Service manager | systemd | 保证服务顺序和长期运行。 / Keeps services ordered and running. |

## 常用命令 | Common Commands

```bash
python cloud_drive_server.py --host 127.0.0.1 --port 8787
python cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s tests
```

```bash
sudo systemctl status lobe-chat.service --no-pager
sudo systemctl status cloud-gateway.service --no-pager
sudo systemctl status cloudflared.service --no-pager
docker ps -a
ls -la ~/.cloudflared
sudo cat /etc/systemd/system/cloudflared.service
```

## 下一步 | Next Step

服务器运行层已经切到 token tunnel。现在只剩一个外部前置条件：  
The server runtime is already on a token tunnel. Only one external prerequisite remains:

- 在 Cloudflare Dashboard 里把真实域名的 public hostname 绑定到这个 tunnel。  
  Bind real-domain public hostnames to this tunnel in the Cloudflare Dashboard.
