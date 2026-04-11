# Sihan's Blog | 思涵的个人网站

> 一个把 AI 对话入口、个人云盘和静态文档站点放在同一套基础设施里的个人项目。

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick-orange)

## 在线入口

| 服务 | 地址 | 说明 |
|------|------|------|
| AI 对话平台 | https://procurement-trying-beside-beginning.trycloudflare.com | LobeChat 主界面 |
| 云盘 | https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive | 文件浏览、上传、下载、建目录、删除 |
| 项目主页 | https://sihan-bzwj.github.io/ | GitHub Pages + MkDocs 文档站点 |
| 仓库地址 | https://github.com/sihan-bzwj/sihan-bzwj.github.io | 源码与部署配置 |

> Cloudflare Quick Tunnel 地址会在隧道重建后变化，实际访问前请以当前运行配置为准。

## 项目功能

### AI 对话平台

- 使用 LobeChat 提供统一的 AI 对话入口。
- 通过云端网关把 AI 服务、云盘服务和静态站点统一暴露到公网。
- 保留独立部署边界，便于后续替换模型提供方或调整网关规则。

### 云盘服务

- 支持目录浏览、文件上传、文件下载、创建目录和删除文件/目录。
- 上传和删除操作依赖同一个服务端密码。
- 目录和下载路径都做了根目录约束，避免越界访问。

### 文档站点

- 使用 MkDocs + GitHub Pages 承载项目主页。
- 页脚通过网关暴露的 `/api/visitor-count` 接口显示访客计数。

## 仓库结构

```text
.
├─ README.md
└─ my-project/
   ├─ cloud_drive_server.py
   ├─ cloud_gateway.py
   ├─ cloud_drive_app/
   │  ├─ config.py
   │  ├─ http_utils.py
   │  ├─ service.py
   │  ├─ storage.py
   │  └─ uploads.py
   ├─ cloud_gateway_app/
   │  ├─ config.py
   │  ├─ proxy.py
   │  ├─ routing.py
   │  ├─ static_site.py
   │  └─ visitors.py
   ├─ docs/
   ├─ tests/
   ├─ cloud-drive.service
   ├─ cloud-gateway.service
   └─ mkdocs.yml
```

## 本次更新记录

### 2026-04-11

- 清理了根目录 `README.md`，删除重复、过长和与真实实现不一致的说明，统一由这份文档记录本次更新。
- 将 `my-project/cloud_drive_server.py` 拆分为 `cloud_drive_app` 包，把配置、路径处理、HTTP 响应、上传解析和文件操作分离成独立模块。
- 将 `my-project/cloud_gateway.py` 拆分为 `cloud_gateway_app` 包，把访客计数、静态站点服务、代理转发和路由规则拆成独立模块。
- 保留原有入口文件名 `cloud_drive_server.py` 和 `cloud_gateway.py`，因此现有 `systemd` 启动命令无需修改。
- 给新模块补充了函数级注释和类说明，便于后续维护和排错。
- 新增标准库单元测试，覆盖云盘路径安全、唯一文件名生成、上传落盘、目录排序、代理路由和访客计数持久化。
- 重写了 `my-project/README.md` 和 `my-project/docs/cloud-drive.md`，删除未实现的“重命名、分享链接、压缩下载、10GB 限制、批量/断点下载”等描述。

## 当前实现边界

- 云盘当前没有重命名接口。
- 云盘当前没有分享链接、过期分享、压缩打包下载和权限分级。
- AI 站点能力主要由 LobeChat 与其上游配置决定，这个仓库关注的是入口聚合、网关转发和文档承载。

## 运行与验证

在 `my-project` 目录下：

```bash
python cloud_drive_server.py --host 127.0.0.1 --port 8787
python cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s tests
```

当前已完成的本地验证命令：

```bash
python -m unittest discover -s tests
```

## 维护说明

- `cloud_drive_server.py` 和 `cloud_gateway.py` 现在是薄入口，业务逻辑优先改对应包目录。
- 如果要修改云盘路径、安全策略或上传行为，优先查看 `cloud_drive_app/`。
- 如果要修改路由、静态站点托管或访客统计，优先查看 `cloud_gateway_app/`。
- 文档站点内容在 `my-project/docs/`，样式和页脚脚本分别在 `docs/stylesheets/extra.css` 与 `docs/javascripts/site-footer.js`。

## 备注

- `my-project/README.md` 现在只保留子项目实现说明，避免和根 README 重复。
- 推送前请确保本地没有真实 API 密钥、上传密码或私有数据被误提交。
