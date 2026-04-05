# 云端 AI 对话平台 + 个人云盘

> 一个完整的 LobeChat 云部署方案 + Python 云盘服务，支持多个 LLM 供应商和文件存储，通过 Cloudflare 隧道 24/7 公网访问。

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick-orange)

---

## 🎯 项目概览

这是一个**完整的云端服务平台**，提供两大核心服务：

### 🤖 AI 对话平台 (LobeChat)
- ✅ **LobeChat** - 多模型 AI 对话平台（Next.js + Node.js）
- ✅ **56+ LLM 供应商** - OpenRouter、OpenAI、Anthropic、DeepSeek 等
- ✅ **动态模型获取** - 自动同步最新模型列表
- ✅ **API 密钥代理** - 安全的后端代理架构

### 💾 个人云盘 (Cloud Drive)
- ✅ **文件管理** - 上传、下载、删除、重命名文件
- ✅ **目录树结构** - 完整的文件夹管理
- ✅ **密码保护** - 支持上传密码验证
- ✅ **Web 前端** - 美观的响应式界面

### 🌐 整体特性
- ✅ **24/7 公网访问** - Cloudflare 隧道自动化部署
- ✅ **Landing Page** - GitHub Pages + MkDocs 项目介绍
- ✅ **完全自动化** - systemd 服务自管理、Docker 自动重启
- ✅ **双服务部署** - LobeChat + Cloud Drive 协作运行

### AI 对话核心特性

| 特性 | 说明 |
|------|------|
| **多模型支持** | 一个界面接入 50+ 个 LLM 模型源 |
| **动态模型获取** | 自动从供应商 API 同步最新模型列表 |
| **安全架构** | API 密钥在后端处理，前端无法访问 |
| **用户可定制** | 用户在前端输入 API 密钥，后端代理请求 |
| **自动化运维** | systemd 服务自动管理，异常自动重启 |
| **国际访问** | Cloudflare Quick Tunnel，免费 24/7 |

### 云盘核心特性

| 特性 | 说明 |
|------|------|
| **文件上传** | Web 界面拖拽或点击上传，支持批量操作 |
| **文件管理** | 创建文件夹，重命名，删除，修改权限 |
| **密码保护** | 上传操作需要密码验证（默认：sihan123） |
| **目录树展示** | 完整的文件夹结构和大小显示 |
| **直链下载** | 支持文件直链访问和下载 |
| **自动化部署** | systemd 服务自动启动和管理 |

---

## 🚀 快速开始

### 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **AI 对话平台** | https://raised-telling-ppm-notre.trycloudflare.com | LobeChat 主界面 |
| **云盘** | https://raised-telling-ppm-notre.trycloudflare.com/cloud-drive | 文件管理 |
| **项目主页** | https://sihan-bzwj.github.io/-sihan-bzwj-.github.io/ | 介绍页面 |

### AI 对话平台使用流程

1. **访问** → https://raised-telling-ppm-notre.trycloudflare.com
2. **设置** → 左下角 Settings → Model Providers
3. **选择供应商** → OpenRouter / OpenAI / Anthropic 等
4. **输入 API 密钥** → 获取方式见下方
5. **开始对话** → 选择模型 → 开始聊天

### 云盘使用流程

1. **访问** → https://raised-telling-ppm-notre.trycloudflare.com/cloud-drive
2. **查看文件** → 显示根目录 /cloud-drive 下的所有文件和文件夹
3. **上传文件** → 点击上传按钮或拖拽文件（需要输入密码）
4. **创建文件夹** → 点击"新建文件夹"按钮
5. **管理操作** → 删除、重命名、下载文件

### 获取 API 密钥

| 供应商 | 网址 | 特点 |
|--------|------|------|
| **OpenRouter** | https://openrouter.ai/keys | 聚合多家模型，推荐 |
| **OpenAI** | https://platform.openai.com/api-keys | GPT-4、GPT-3.5 |
| **Anthropic** | https://console.anthropic.com/ | Claude 家族 |
| **Google Gemini** | https://ai.google.dev/ | Gemini 模型 |
| **DeepSeek** | https://www.deepseek.com/ | 国内大模型 |
| **Mistral AI** | https://console.mistral.ai/ | 开源模型 |
| **Groq** | https://console.groq.com/ | 高速推理 |

更多供应商支持，见下方架构说明。

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│              用户浏览器 (Web 客户端)                      │
│              国际用户 / 国内用户                         │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTPS 请求
                   ▼
    ┌──────────────────────────────────┐
    │   Cloudflare Quick Tunnel        │
    │  (国际隧道 - 免费，24/7)         │
    │ raised-telling-ppm-notre...      │
    │    trycloudflare.com             │
    └──────────────┬───────────────────┘
                   │ HTTP 转发
                   ▼
    ┌───────────────────────────────────────────────────────┐
    │      Azure Linux VM (IP: 20.196.193.8)               │
    │                                                       │
    │  ┌────────────────────────────────────────────────┐  │
    │  │   LobeChat Docker 容器                         │  │
    │  │  (Next.js 前端 + Node.js 后端)               │  │
    │  │  端口: 3210                                    │  │
    │  └────────────────────────────────────────────────┘  │
    │                                                       │
    │  ┌────────────────────────────────────────────────┐  │
    │  │  Cloud Drive Python 服务                       │  │
    │  │  (Flask/HTTP 服务器)                          │  │
    │  │  端口: 8787 (内部)                            │  │
    │  │  访问: https://.../cloud-drive                │  │
    │  └────────────────────────────────────────────────┘  │
    │                                                       │
    │  ┌────────────────────────────────────────────────┐  │
    │  │  cloudflared (systemd 服务)                    │  │
    │  │  自动重启、日志管理                            │  │
    │  └────────────────────────────────────────────────┘  │
    │                                                       │
    │  数据存储:                                           │
    │  • /home/azureuser/lobe-chat.env (环境变量)        │
    │  • /home/azureuser/cloud-drive/ (文件系统)        │
    │                                                       │
    └───────────────────────────────────────────────────────┘
                   ▲
        ┌──────────┴───────────────────┐
        │  外部 LLM API 供应商          │
        │  OpenRouter / OpenAI / etc    │
        │  (56+ 供应商)                 │
        └───────────────────────────────┘
```

### AI 对话工作原理

```
用户输入消息
    ↓
LobeChat 前端 (JavaScript) 显示
    ↓
POST /chat 到后端 (Node.js)
    ↓
后端验证 API 密钥
    ↓
调用对应供应商 API
    ↓
流式返回 AI 响应
    ↓
前端实时显示
    ↓
存储到本地或数据库
```

### 云盘操作流程

```
用户在浏览器打开云盘页面
    ↓
Cloud Drive Python 后端列出 /cloud-drive 目录
    ↓
前端渲染文件树
    ↓
用户上传文件
    ↓
验证上传密码
    ↓
文件保存到 /home/azureuser/cloud-drive/
    ↓
刷新文件列表显示新文件
```

### 为什么 API 密钥必须在后端

- ❌ **前端暴露密钥** → 任何人可以盗用你的账户
- ✅ **后端代理** → 密钥在服务器，前后端通信加密
- ✅ **安全性高** → 用户将认证信息安全委托给服务器

---

## 🔧 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **前端** | Next.js | 15.3.8 | AI 对话 UI |
| **后端-AI** | Node.js | Built-in | API 代理 |
| **后端-云盘** | Python | 3.11+ | 文件管理 |
| **容器** | Docker | v26+ | 应用隔离和部署 |
| **隧道** | Cloudflare | v2026.3.0 | 公网访问 |
| **服务管理** | systemd | Linux native | 自动启停和重启 |
| **网站** | MkDocs + GitHub Pages | Latest | Landing page |
| **版本控制** | Git | Built-in | 代码管理 |

---

## ⚙️ 核心配置

### LobeChat 环境变量 (`lobe-chat.env`)

```bash
NODE_ENV=production          # 生产模式
HOSTNAME=0.0.0.0           # 监听所有网卡
PORT=3210                  # 容器内端口

# 54 个供应商的 API 密钥和模型列表
# 用户在前端填入，或预配置在此
OPENROUTER_API_KEY=        # 用户输入
OPENROUTER_MODEL_LIST=     # 空 = 动态获取
OPENAI_API_KEY=            # 用户输入
OPENAI_MODEL_LIST=         # 空 = 动态获取
ANTHROPIC_API_KEY=         # 用户输入
...                        # (51 个其他供应商)
```

### Cloud Drive 服务配置 (`cloud-drive.service`)

```ini
[Unit]
Description=Cloud Drive API
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser
Environment="CLOUD_DRIVE_ROOT=/home/azureuser/cloud-drive"
ExecStart=/usr/bin/python3 /home/azureuser/bin/cloud_drive_server.py \
          --host 127.0.0.1 --port 8787 --root /home/azureuser/cloud-drive
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=cloud-drive

[Install]
WantedBy=multi-user.target
```

### Cloudflare 隧道服务 (`cloudflared.service`)

```ini
[Unit]
Description=Cloudflare Tunnel for LobeChat + Cloud Drive
After=network.target

[Service]
Type=simple
User=azureuser
ExecStart=/usr/bin/cloudflared tunnel --url http://localhost:3210
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 📊 部署工作流

### 5 阶段部署清单

| 阶段 | 内容 | 状态 |
|------|------|------|
| **1. 基础设施** | Azure VM、Docker、SSH 密钥 | ✅ |
| **2. LobeChat** | 拉取镜像、配置环境变量、启动容器 | ✅ |
| **3. Cloud Drive** | Python 服务、systemd 配置、权限设置 | ✅ |
| **4. Cloudflare** | cloudflared 隧道、systemd 服务 | ✅ |
| **5. Landing Page** | MkDocs 项目介绍、GitHub Pages 部署 | ✅ |

### 关键运维命令

```bash
# ========== LobeChat 命令 ==========
# 查看 LobeChat 状态
docker ps -f name=lobe-chat

# 查看 LobeChat 日志
docker logs -f lobe-chat

# 重启 LobeChat
docker restart lobe-chat

# 进入容器调试
docker exec -it lobe-chat /bin/bash

# ========== Cloud Drive 命令 ==========
# 查看 Cloud Drive 状态
systemctl status cloud-drive.service

# 查看 Cloud Drive 日志
journalctl -u cloud-drive -f

# 重启 Cloud Drive
sudo systemctl restart cloud-drive.service

# ========== Cloudflare 隧道命令 ==========
# 查看隧道状态
systemctl status cloudflared.service

# 查看隧道日志和实时地址
journalctl -u cloudflared -f

# 重启隧道
sudo systemctl restart cloudflared.service

# 获取当前隧道 URL
grep -Eo "https://.*\.trycloudflare\.com" /var/log/syslog | tail -1
```

---

## 🔐 模型供应商配置

### 动态 API 获取原理

```
容器启动
    ↓
读取环境变量 *_API_KEY 和 *_MODEL_LIST
    ↓
如果 API_KEY 为空 → 前端显示输入框
    ↓
如果 MODEL_LIST 为空 → 从 API 动态获取（推荐）
    ↓
前端显示最新的模型列表
    ↓
用户选择模型 → 发送到后端 → 调用对应 API
```

### 已支持的供应商 (56 个)

**主流模型源**:
- OpenRouter (聚合)
- OpenAI (GPT 系列)
- Anthropic (Claude)
- Google (Gemini)
- Mistral AI
- Groq
- DeepSeek
- Perplexity
- Cohere

**其他供应商**: AI21、Baichuan、Azure、Hugging Face、Ollama、Qwen、Wenxin、Spark 等...

---

## ⚠️ 已知限制与优化方向

### 现有限制

| 限制 | 原因 | 影响 |
|------|------|------|
| **地址变化** | Quick Tunnel 免费方案 | 重启时隧道地址可能变化 |
| **国际延迟** | Cloudflare 节点位置 | 100-300ms 延迟 |
| **流量限制** | 免费方案限制 | 正常个人使用足够 |
| **存储限制** | 单机存储 | 云盘大小受 Azure VM 磁盘限制 |

### 优化方向

- [ ] **自定义域名** - 升级到 Cloudflare 付费隧道
- [ ] **国内加速** - Cpolar/Frp 方案到国内 VPS
- [ ] **缓存优化** - CDN + 客户端缓存
- [ ] **数据持久化** - 云数据库（Azure Cosmos DB）
- [ ] **监控告警** - Prometheus + Grafana 统计
- [ ] **备份策略** - 自动备份 cloud-drive 到 Azure Storage
- [ ] **权限管理** - 多用户、权限控制
- [ ] **API 文档** - OpenAPI / Swagger 规范

---

## 📁 项目目录结构

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml                 # MkDocs 自动部署
│
├── docs/                              # MkDocs 源文件
│   ├── index.md                       # 首页（landing page）
│   ├── cloud-drive.md                 # 云盘使用说明
│   └── stylesheets/
│       └── extra.css                  # 自定义样式
│
├── cloud_drive_server.py              # Cloud Drive Python 服务
├── cloud-drive.service                # Cloud Drive systemd 配置
├── cloud-drive-tunnel.service         # Cloud Drive 隧道配置
│
├── mkdocs.yml                         # MkDocs 配置
├── README.md                          # 本文件
└── .gitignore                         # Git 忽略规则
```

---

## 🤝 贡献和反馈

Issues、PRs 欢迎！如有问题或建议，请在 GitHub Issues 中提出。

---

## 📖 相关资源

### 官方文档
- **LobeChat** - https://docs.lobechat.com/
- **Cloudflare Tunnel** - https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- **MkDocs** - https://www.mkdocs.org/

### 模型供应商
- **OpenRouter** - https://openrouter.ai/
- **OpenAI** - https://openai.com/
- **Anthropic** - https://www.anthropic.com/
- **Google DeepMind** - https://deepmind.google/

---

## 📝 更新日志

最新更新信息见本 README

---

## 📄 许可证

MIT License

---

**最近更新**: 2026年4月5日  
**维护者**: @sihan-bzwj  
**在线访问**: https://raised-telling-ppm-notre.trycloudflare.com
