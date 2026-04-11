# my-project

这个目录放项目的实际服务代码、文档站点和部署文件。

根目录 [README.md](../README.md) 是当前唯一的总入口和更新记录；这里不再重复维护一份长说明，避免文档分叉。

## 目录说明

- `cloud_drive_server.py`：云盘 HTTP 服务入口，负责启动服务。
- `cloud_gateway.py`：云网关入口，负责静态站点、AI 入口和云盘入口的统一转发。
- `cloud_drive_app/`：云盘服务的配置、路径处理、上传解析、响应工具和业务逻辑。
- `cloud_gateway_app/`：网关服务的配置、访客计数、代理转发、静态文件服务和路由规则。
- `docker-compose.lobechat.yml`：LobeChat 容器编排文件，供云服务器启动 AI 平台使用。
- `lobe-chat.service`：LobeChat 的 `systemd` 服务定义。
- `.env.lobechat.example`：远程服务器环境变量模板。
- `docs/`：MkDocs 站点内容。
- `tests/`：本次重构新增的标准库单元测试。
- `cloud-drive.service` / `cloud-gateway.service`：Linux `systemd` 部署配置。

## 常用命令

```bash
python cloud_drive_server.py --host 127.0.0.1 --port 8787
python cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s tests
```

云服务器启动 AI 平台：

```bash
cp .env.lobechat.example /home/azureuser/.env.lobechat
cp docker-compose.lobechat.yml /home/azureuser/docker-compose.lobechat.yml
sudo cp lobe-chat.service /etc/systemd/system/lobe-chat.service
sudo systemctl daemon-reload
sudo systemctl enable --now lobe-chat.service
sudo systemctl restart cloud-gateway.service
```

## 本次重构重点

- 入口脚本保留不变，部署脚本无需跟着重写。
- 通用逻辑拆到包目录中，减少单文件多职责问题。
- 文档只保留已实现能力，避免页面和代码描述不一致。
- 远程服务器现在有独立的 AI 平台启动配置，不再只依赖网关假设 `127.0.0.1:3210` 已经存在。
