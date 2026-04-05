# 项目完整说明和更新日志

---

## 📘 项目原理和架构

### 🎯 项目目标
搭建一个**云端 AI 对话平台 + 个人博客 landing page** 的完整系统，支持多个 LLM 供应商（OpenAI、Anthropic、DeepSeek 等），通过国际隧道 24/7 公网访问。

### 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户浏览器                              │
│              (Web 客户端 - 国际用户)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS 请求
                       ▼
        ┌──────────────────────────────────┐
        │   Cloudflare Quick Tunnel        │
        │  (国际隧道 - 免费，24/7)         │
        │ raised-telling-ppm-notre...      │
        │  trycloudflare.com               │
        └──────────────┬───────────────────┘
                       │ HTTP 转发
                       ▼
        ┌──────────────────────────────────────────────────────┐
        │        Azure Linux VM (20.196.193.8)                │
        │                                                      │
        │  ┌────────────────────────────────────────────────┐ │
        │  │      LobeChat Docker 容器                      │ │
        │  │  (Next.js 前端 + Node 后端)                   │ │
        │  │  端口: 3210                                    │ │
        │  │                                                │ │
        │  │  功能:                                         │ │
        │  │  • AI 多模型对话                              │ │
        │  │  • 模型提供商动态获取                          │ │
        │  │  • 前端输入 API 密钥                          │ │
        │  │  • 消息管理、设置等                           │ │
        │  └────────────────────────────────────────────────┘ │
        │                                                      │
        │  ┌────────────────────────────────────────────────┐ │
        │  │   cloudflared systemd 服务                     │ │
        │  │  (隧道客户端 - 自动重启)                      │ │
        │  │                                                │ │
        │  └────────────────────────────────────────────────┘ │
        │                                                      │
        │  数据存储:                                          │
        │  • /home/azureuser/lobe-chat.env (环境变量)       │
        │  • docker 容器持久化存储                          │
        │                                                      │
        └──────────────────────────────────────────────────────┘
                       ▲
        ┌──────────────┴────────────────────┐
        │   GitHub Pages + MkDocs            │
        │  (landing page / 个人博客)         │
        │  https://sihan-bzwj.github.io/    │
        │                                    │
        │  原理: docs/ → mkdocs → GitHub     │
        │       Actions → gh-pages 分支      │
        └────────────────────────────────────┘

                   外部 LLM API
        ┌────────────────────────────────────┐
        │  OpenRouter         (openrouter.ai) │
        │  OpenAI            (openai.com)    │
        │  Anthropic         (claude...)     │
        │  Google Gemini     (google.com)    │
        │  Mistral           (mistral.ai)    │
        │  DeepSeek          (deepseek.com)  │
        │  (+ 50+ 其他供应商)                 │
        │                                    │
        │  认证: 用户在前端输入 API 密钥     │
        │  传输: 从 LobeChat 后端代理请求    │
        └────────────────────────────────────┘
```

### 🔄 数据流原理

#### LLM 对话流程
```
用户输入消息
     ↓
浏览器 JavaScript → LobeChat 前端显示
     ↓
POST /chat 到 LobeChat 后端 (Node.js)
     ↓
后端验证 API 密钥（来自:环境变量 或 前端)
     ↓
根据模型类型生成 API 请求
     ↓
调用对应供应商 API (OpenRouter/OpenAI/etc)
     ↓
流式返回 AI 响应
     ↓
LobeChat 前端实时显示
     ↓
存储到本地存储 (IndexedDB) 或数据库
```

#### 为什么 API 密钥不能在前端处理
- ❌ 前端暴露密钥 → 任何人可盗用你的账户
- ❌ 前端加密密钥 → 但解密密钥仍在浏览器中，无法真正保护
- ✅ 后端代理 → 密钥在服务器，前后端通信加密

### 🔐 模型供应商配置原理

#### 动态 API 获取模式
```
LobeChat 容器启动
     ↓
读取环境变量: *_API_KEY, *_MODEL_LIST
     ↓
如果 API_KEY 为空 → 前端显示输入框（用户填密钥）
     ↓
如果 API_KEY 有值 → 启动时从 API 获取完整模型列表
     ↓
*_MODEL_LIST 为空 → 从 API 动态获取（推荐）
*_MODEL_LIST 有值 → 使用硬编码列表（之前的方案）
     ↓
前端模型选择器 → 显示可用模型
     ↓
用户选择模型 → 发送到后端 → 调用对应 API
```

当前配置：
- **56 个供应商**: AI21、Anthropic、Google、Mistral、OpenRouter、DeepSeek 等
- **所有 _MODEL_LIST 为空**: 激活动态 API 获取模式
- **所有 _API_KEY 为空**: 等待用户在前端输入

---

## 🚀 关键技术栈

| 组件 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **前端框架** | Next.js | 15.3.8 | LobeChat UI 和响应式设计 |
| **后端运行时** | Node.js | Built-in | LobeChat 后端服务 |
| **容器化** | Docker | v26+ | 隔离环境、便捷部署 |
| **隧道** | Cloudflare Quick Tunnel | v2026.3.0 | 国际公网访问 |
| **服务管理** | systemd | Linux native | cloudflared 自动管理 |
| **静态网站** | MkDocs + GitHub Pages | md to html | landing page |
| **Git 版本控制** | Git | Built-in | 代码和配置管理 |

---

## 🔧 核心配置文件

### 1. `/home/azureuser/lobe-chat.env`
- **作用**: Docker 容器的所有环境变量
- **关键变量**:
  - `NODE_ENV=production` - 生产模式
  - `HOSTNAME=0.0.0.0` - 监听所有网卡
  - `PORT=3210` - 容器内监听端口
  - `*_API_KEY` - 各供应商密钥（56 个）
  - `*_MODEL_LIST` - 各供应商模型列表（56 个）

### 2. `/etc/systemd/system/cloudflared.service`
- **作用**: 管理 cloudflared 守护进程
- **特性**:
  - `Restart=always` - 异常退出自动重启
  - `User=azureuser` - 以 azureuser 用户运行
  - `ExecStart=/home/azureuser/bin/cloudflared-start.sh` - 启动脚本

### 3. `/home/azureuser/bin/cloudflared-start.sh`
- **作用**: 启动 cloudflared 隧道
- **命令**: `cloudflared tunnel --url http://localhost:3210`
- **输出**: 日志存储到 `/home/azureuser/cloudflared.log`

---

## 🔄 部署工作流

### 第 1 阶段：基础设施 (已完成)
1. ✅ Azure VM 创建 (Linux, Ubuntu 20+)
2. ✅ Docker 安装和配置
3. ✅ SSH 密钥对生成
4. ✅ 防火墙规则（开放 3210 等）

### 第 2 阶段：LobeChat 部署 (已完成)
1. ✅ 拉取 lobehub/lobe-chat:latest 镜像
2. ✅ 生成环境变量文件 (56 个供应商配置)
3. ✅ 运行容器: `docker run ... -p 3210:3210 --env-file lobe-chat.env ...`
4. ✅ 配置 docker restart policy (unless-stopped)

### 第 3 阶段：隧道配置 (已完成)
1. ✅ 下载 cloudflared 二进制
2. ✅ 创建 systemd 服务单元
3. ✅ 启动隧道: `systemctl start cloudflared.service`
4. ✅ 获得公网地址: `https://raised-telling-ppm-notre.trycloudflare.com`

### 第 4 阶段：landing page (已完成)
1. ✅ 初始化 MkDocs 项目
2. ✅ 创建 docs/index.md (中英双语)
3. ✅ 部署到 GitHub Pages: `mkdocs gh-deploy`
4. ✅ 发布地址: https://sihan-bzwj.github.io/-sihan-bzwj-.github.io/

### 第 5 阶段：模型配置 (已完成)
1. ✅ 清空所有 `_MODEL_LIST` 硬编码值
2. ✅ 保持所有 `_API_KEY` 为空（前端输入）
3. ✅ 重启容器应用配置

---

## 📊 系统监控和维护

### 常用命令

```bash
# 查看容器状态
docker ps -f name=lobe-chat

# 查看容器日志
docker logs lobe-chat --tail 100

# 查看隧道状态
systemctl status cloudflared.service

# 查看隧道日志
journalctl -u cloudflared -f

# 重启 LobeChat
docker restart lobe-chat

# 重启隧道
systemctl restart cloudflared.service

# 修改 api key 后重启容器
docker rm -f lobe-chat
docker run -d --name lobe-chat --restart unless-stopped -p 3210:3210 \
  --env-file /home/azureuser/lobe-chat.env lobehub/lobe-chat:latest
```

---

## 🎯 使用指南

### 快速开始
1. 访问: `https://raised-telling-ppm-notre.trycloudflare.com`
2. 左下角 **Settings** → **Model Providers**
3. 选择模型供应商（如 OpenRouter）
4. 输入 API 密钥
5. 返回聊天界面，选择模型开始对话

### API 密钥获取
- **OpenRouter**: https://openrouter.ai/keys
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google Gemini**: https://ai.google.dev/
- 其他供应商...

---

## ⚠️ 已知限制和未来优化

### 现有限制
- Cloudflare Quick Tunnel 地址不稳定（每次重启变化）
- 国际延迟较高（100-300ms）
- 免费方案有流量限制

### 优化方向
1. **自定义域名**: 升级 Cloudflare 付费版或使用 CNAME
2. **国内隧道**: 部署 Cpolar/Frp 到国内 VPS（需购买）
3. **缓存优化**: 启用 LobeChat CDN 和客户端缓存
4. **数据库**: 迁移到云数据库（持久化对话记录）
5. **监控告警**: Prometheus + Grafana（资源监控）

---

## 2026-04-05 - 首页应用入口模块重构

### 📋 更新概述
完整重构了首页设计，将 LobeChat 和 Cloud Drive 作为核心应用入口展示，统一了整站视觉风格。

### 🎯 更新目标
1. **提升应用可发现性**: 为两大核心服务（AI 和云盘）创建独立的介绍模块
2. **统一视觉语言**: 从分散的内联样式迁移到统一的外部CSS框架
3. **优化用户体验**: 使用卡片式设计展示服务特点和快速操作入口

### ✨ 主要改动

#### 1. 首页结构调整 (`docs/index.md`)
- **删除**: 移除了冗长的内联CSS样式（约200行）
- **新增**: "应用入口" (Applications) section，包含两个服务卡片
  - **AI 站点卡片**
    - 标签: `Tool · AI`
    - 描述: 基于 LobeChat 搭建的多模型对话平台
    - 特性: 支持本地模型、云端API、快速切换、自定义配置
    - 操作按钮: 进入 AI 站点、了解 LobeChat
  - **Cloud Drive 卡片**
    - 标签: `Storage · Cloud`
    - 描述: 远程文件存储和共享服务
    - 特性: 大文件支持、密码保护上传、无限制下载
    - 操作按钮: 打开云盘、了解更多

#### 2. 样式系统建设 (`docs/stylesheets/extra.css`)
- **创建**: 新的外部CSS文件，集中管理所有主题和组件样式
- **核心样式**:
  - `.site-shell`: 主体容器，带渐变背景和网格图案
  - `.card` + `.info-panel`: 服务卡片容器
  - `.card-header`: 卡片标题区域（标签 + 标题）
  - `.card-actions`: 卡片操作按钮组（使用 flexbox + margin-top: auto）
  - `.button` / `.button-secondary`: 主次按钮样式
  - 统一的颜色方案、间距、排版系统

#### 3. 配置文件更新 (`mkdocs.yml`)
```yaml
# 主要改动
site_name: Axi's Blog                              # 从 LobeChat 入口 改为个人博客品牌
extra_css:                                         # 登记外部CSS文件
  - stylesheets/extra.css
nav:
  - 首页 / Home: index.md
  - 云盘 / Cloud Drive: cloud-drive.md
  - AI 站点 / AI: https://raised-telling-ppm-notre.trycloudflare.com  # 新增外链
```

#### 4. 文档同步 (`PROJECT_CONTEXT.md`)
- 更新 UX 设计模式，记录"内容入口 + 应用入口"的二段式结构
- 补充视觉系统文档，说明卡片设计、CSS模式、responsive 布局
- 标记所需更新的关键文件

### 🏗️ 架构演进

**之前** (inline styles):
```
docs/index.md (包含 200+ 行内联 CSS)
    ↓
过度耦合，难以维护和复用
```

**现在** (external stylesheet):
```
docs/index.md (纯 HTML/Markdown 结构)
    ↓
docs/stylesheets/extra.css (统一的 CSS 框架)
    ↓
mkdocs.yml (在 extra_css 中注册)
    ↓
site/ (静态输出)
```

### 📊 改动统计
- **文件修改**: 4 个主要文件
- **新增文件**: 1 个 (docs/stylesheets/extra.css)
- **代码行数**: +735 插入, -463 删除 (净增 272 行)
- **关键改进**: 1 个新CSS框架，2 个服务卡片模块，统一品牌形象

### 🚀 部署流程
1. ✅ 本地完成所有改动和测试 (`mkdocs build` 成功)
2. ✅ 提交更改到 Git (`git commit` with detailed message)
3. ✅ 推送到 GitHub (`git push origin main`)
4. ⏳ GitHub Actions 自动触发 (`.github/workflows/deploy.yml`)
   - 运行 `mkdocs gh-deploy --force`
   - 自动更新 `gh-pages` 分支
   - 线上网站自动更新：https://sihan-bzwj.github.io/-sihan-bzwj-.github.io/

### 💡 设计决策说明

**Q: 为什么要将样式从内联移出到外部CSS?**
- 内联样式在Markdown中难以维护和复用
- 外部CSS支持更好的模块化和一致性
- 便于后续的主题切换和扩展

**Q: 为什么采用卡片式布局?**
- 清晰展示每个服务的核心价值
- 视觉上分离了"内容"和"应用"两个维度
- 便于未来添加更多服务/工具

**Q: 如何实现卡片底部按钮对齐?**
- 使用 flexbox: `display: flex; flex-direction: column;`
- 按钮容器: `.card-actions { margin-top: auto; }`
- 这样无论内容多少，按钮都自动沉底

### 🔄 后续维护指南

**如果要修改应用卡片**:
1. 编辑 `docs/index.md` 中的 `#applications` section
2. 直接修改HTML结构（卡片内容、按钮、标签）
3. 运行 `mkdocs build` 测试
4. 提交并push自动部署

**如果要修改卡片样式**:
1. 编辑 `docs/stylesheets/extra.css`
2. 调整 `.card`, `.card-header`, `.info-panel`, `.card-actions` 等类
3. 运行 `mkdocs build` 验证
4. 提交并push自动部署

**如果要添加更多服务**:
1. 在 `#applications` 中复制一个卡片
2. 更新内容、标签、按钮链接
3. 确保 `.cards` 容器的网格适应新数量（默认3列）
4. 如需调整布局，在 `extra.css` 中修改 `.cards { grid-template-columns: ... }`

### 📝 提交信息解读
```
feat: redesign homepage with services showcase
```
采用 Conventional Commits 格式，清晰记录：
- `feat`: 新功能性改进（应用卡片模块）
- 详细 body: 逐行记录各个改动及其目的
- 特别标记: BREAKING（样式迁移）、VISUAL（视觉变化）、A11Y（可访问性）

### ✅ 验证清单
- [x] 本地构建成功
- [x] 视觉设计符合预期 (screenshot: 两张卡片并排展示)
- [x] 所有链接可正常访问
- [x] CSS 类名一致性检查
- [x] 响应式布局测试
- [x] Git commit 消息清晰完整
- [x] Push 到 main 分支成功
- [x] GitHub Actions 自动部署触发

### 📍 下一步建议
1. 监控 GitHub Actions 部署状态（点击 Actions 标签查看）
2. 部署完成后（约 1-2 分钟）刷新线上网站确认更新
3. 如果有问题，可快速修改后重新push
4. 考虑为其他页面（cloud-drive.md）应用相同的卡片设计模式
