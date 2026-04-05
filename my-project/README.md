# 云端 AI 对话平台 + Landing Page

> 一个完整的 LobeChat 云部署方案，支持多个 LLM 供应商，通过 Cloudflare 隧道 24/7 公网访问。

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick-orange)

---

## 🎯 项目概览

这是一个**完整的云端 AI 聊天系统**，包含：

- ✅ **LobeChat** - 多模型 AI 对话平台（Next.js + Node.js）
- ✅ **56+ LLM 供应商** - OpenRouter、OpenAI、Anthropic、DeepSeek 等
- ✅ **24/7 公网访问** - Cloudflare 隧道自动化部署
- ✅ **Landing Page** - GitHub Pages + MkDocs 项目介绍
- ✅ **完全自动化** - systemd 服务自管理、Docker 自动重启

### 核心特性

| 特性 | 说明 |
|------|------|
| **多模型支持** | 一个界面接入 50+ 个 LLM 模型源 |
| **动态模型获取** | 自动从供应商 API 同步最新模型列表 |
| **安全架构** | API 密钥在后端处理，前端无法访问 |
| **用户可定制** | 用户在前端输入 API 密钥，后端代理请求 |
| **自动化运维** | systemd 服务自动管理，异常自动重启 |
| **国际访问** | Cloudflare Quick Tunnel，免费 24/7 |

---

## 🚀 快速开始

### 访问地址

**在线访问**: https://raised-telling-ppm-notre.trycloudflare.com

**项目主页**: https://sihan-bzwj.github.io/-sihan-bzwj-.github.io/

### 使用流程

1. **访问** → https://raised-telling-ppm-notre.trycloudflare.com
2. **设置** → 左下角 Settings → Model Providers
3. **选择供应商** → OpenRouter / OpenAI / Anthropic 等
4. **输入 API 密钥** → 获取方式见下方
5. **开始对话** → 选择模型 → 开始聊天

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
┌─────────────────────────────────────────┐
│          用户浏览器 (Web 客户端)          │
└──────────────────┬──────────────────────┘
                   │ HTTPS 请求
                   ▼
    ┌──────────────────────────────┐
    │   Cloudflare Quick Tunnel    │
    │  (国际隧道 - 免费，24/7)     │
    │ raised-telling-ppm-notre...  │
    │       trycloudflare.com      │
    └──────────────┬───────────────┘
                   │ HTTP 转发
                   ▼
    ┌──────────────────────────────────────┐
    │    Azure Linux VM (IP: 20.196.193.8) │
    │                                      │
    │  ┌────────────────────────────────┐ │
    │  │   LobeChat Docker 容器         │ │
    │  │ (Next.js 前端 + Node 后端)    │ │
    │  │ 端口: 3210                     │ │
    │  └────────────────────────────────┘ │
    │                                      │
    │  ┌────────────────────────────────┐ │
    │  │  cloudflared (systemd 服务)   │ │
    │  │  自动重启、日志管理            │ │
    │  └────────────────────────────────┘ │
    │                                      │
    └──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
    OpenRouter            OpenAI
    Claude              DeepSeek
    Gemini          (50+ 供应商)
```

### 工作原理

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

### 为什么 API 密钥必须在后端

- ❌ **前端暴露密钥** → 任何人可以盗用你的账户
- ✅ **后端代理** → 密钥在服务器，前后端通信加密
- ✅ **安全性高** → 用户将认证信息安全委托给服务器

---

## 🔧 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **前端** | Next.js | 15.3.8 | UI 和响应式设计 |
| **后端** | Node.js | Built-in | API 处理和代理 |
| **容器** | Docker | v26+ | 隔离和便捷部署 |
| **隧道** | Cloudflare | v2026.3.0 | 国际公网访问 |
| **服务** | systemd | Linux native | 自动管理和重启 |
| **网站** | MkDocs + GitHub Pages | Latest | Landing page |
| **版本控制** | Git | Built-in | 代码管理 |

---

## 📋 核心配置

### 环境变量 (`lobe-chat.env`)

```bash
NODE_ENV=production          # 生产模式
HOSTNAME=0.0.0.0           # 监听所有网卡
PORT=3210                  # 容器内端口

# 56 个供应商的 API 密钥和模型列表
OPENROUTER_API_KEY=        # 用户在前端填入
OPENROUTER_MODEL_LIST=     # 空 = 动态获取
OPENAI_API_KEY=            # 用户在前端填入
OPENAI_MODEL_LIST=         # 空 = 动态获取
...                        # (54 个其他供应商)
```

### systemd 服务 (`cloudflared.service`)

```ini
[Unit]
Description=Cloudflare Tunnel for LobeChat
After=network.target

[Service]
Type=simple
User=azureuser
ExecStart=/home/azureuser/bin/cloudflared tunnel --url http://localhost:3210
Restart=always              # 异常自动重启
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 📊 部署工作流

### 5 阶段部署

| 阶段 | 内容 | 状态 |
|------|------|------|
| **1. 基础设施** | Azure VM、Docker、SSH 密钥 | ✅ |
| **2. LobeChat 容器** | 拉取镜像、配置环境、启动容器 | ✅ |
| **3. 隧道配置** | cloudflared systemd 服务 | ✅ |
| **4. Landing Page** | MkDocs 项目介绍页面 | ✅ |
| **5. 模型配置** | 56 个供应商动态 API 获取 | ✅ |

### 关键命令

```bash
# 查看 LobeChat 状态
docker ps -f name=lobe-chat

# 查看隧道日志
journalctl -u cloudflared -f

# 查看隧道地址
grep -Eo "https://.*\.trycloudflare\.com" /home/azureuser/cloudflared.log | tail -1

# 重启 LobeChat
docker restart lobe-chat

# 重启隧道
systemctl restart cloudflared.service
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

## ⚠️ 已知限制 & 未来优化

### 现有限制

| 限制 | 原因 | 影响 |
|------|------|------|
| **地址变化** | Quick Tunnel 免费方案特性 | 每次重启地址变化 |
| **国际延迟** | Cloudflare 美国节点 | 100-300ms 延迟 |
| **流量限制** | 免费方案限制 | 正常使用足够 |

### 优化方向

- [ ] 自定义域名 (升级 Cloudflare 付费)
- [ ] 国内隧道加速 (Cpolar/Frp 到国内 VPS)
- [ ] 缓存优化 (CDN + 客户端缓存)
- [ ] 数据持久化 (云数据库)
- [ ] 监控告警 (Prometheus + Grafana)

---

## 📁 项目结构

```
my-project/
├── docs/                          # MkDocs 源文件
│   ├── index.md                   # 首页 (landing page)
│   ├── cloud-drive.md             # 云盘介绍
│   └── stylesheets/
│       └── extra.css              # 自定义样式
├── site/                          # MkDocs 构建输出
│   ├── index.html
│   └── ...
├── mkdocs.yml                     # MkDocs 配置
├── UPDATE_LOG.md                  # 项目完整说明和更新日志
├── README.md                      # 本文件
├── cpolar.service                 # Cpolar systemd 配置 (可选)
├── frpc.service                   # Frp systemd 配置 (可选)
└── CPOLAR_DOWNLOAD_DIRECT.md      # Cpolar 部署指南 (可选)
```

---

## 🤝 贡献和反馈

Issues、PRs 欢迎！

如有问题或建议，请在 GitHub Issues 中提出。

---

## 📝 许可

MIT License

---

## 🔗 相关链接

- **LobeChat 主仓库**: https://github.com/lobehub/lobe-chat
- **Cloudflare 文档**: https://developers.cloudflare.com/
- **MkDocs 文档**: https://www.mkdocs.org/
- **Azure 文档**: https://docs.microsoft.com/azure/

---

**Last Updated**: 2026-04-05  
**Deployment Status**: ✅ Active  
**Public URL**: https://raised-telling-ppm-notre.trycloudflare.com

---

<div align="center">

**Made with ❤️ for AI enthusiasts**

</div>
