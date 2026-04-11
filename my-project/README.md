# my-project | 服务、部署与文档源文件
> Service code, deployment files, and MkDocs source.  
> 服务代码、部署文件与 MkDocs 文档源文件。

## 这里放了什么 | What Lives Here

- `cloud_drive_app/`: 云盘配置、存储、上传与业务逻辑 / cloud-drive config, storage, uploads, and business logic
- `cloud_gateway_app/`: 网关配置、代理、静态内容与路由 / gateway config, proxying, static content, and routing
- `cloud_drive_server.py`: 云盘服务入口 / cloud-drive entrypoint
- `cloud_gateway.py`: 网关服务入口 / gateway entrypoint
- `cloud-drive.service`: 云盘 `systemd` 单元 / `systemd` unit for the drive
- `cloud-gateway.service`: 网关 `systemd` 单元 / `systemd` unit for the gateway
- `docs/`: GitHub Pages 文档站源文件 / GitHub Pages documentation source
- `tests/`: 标准库单元测试 / standard-library unit tests

## 当前部署模型 | Current Deployment Model

```text
Public cloud-drive traffic
  -> clouddrive.ccwu.cc
  -> Azure VM public IP
  -> Caddy (:443)
  -> cloud_drive_server.py on 127.0.0.1:8787

Public docs
  -> GitHub Pages
  -> MkDocs build output generated from docs/
```

关键点 | Key Points

- 云盘公网域名由 Caddy 负责 HTTPS。
- The public cloud-drive domain terminates on Caddy.
- 上传文件仍保存在 Azure VM。
- Uploaded files remain on the Azure VM.
- 公共 AI 服务已经不在当前对外部署范围内。
- Public AI is no longer part of the current public deployment.

## 已验证状态 | Server-Verified State

基于 `2026-04-11` 的实际检查：
Based on the actual checks performed on `2026-04-11`:

- `cloud-drive.service`: `active`
- `caddy.service`: `active`
- `cloud-gateway.service`: `active`
- `lobe-chat.service`: `stopped`
- `https://clouddrive.ccwu.cc/health`: `live`

## 文档站前端模块 | Docs Front-End Modules

- `docs/index.md`: 首页内容 / homepage content
- `docs/cloud-drive.md`: 云盘页内容 / cloud-drive page content
- `docs/stylesheets/fonts.css`: 字体配置 / fonts
- `docs/stylesheets/tokens.css`: 主题变量与昼夜配色 / theme tokens and day-night palette
- `docs/stylesheets/base.css`: MkDocs/Material 全局覆盖 / MkDocs/Material base overrides
- `docs/stylesheets/components.css`: 导航、按钮、卡片等通用组件 / shared nav, buttons, and cards
- `docs/stylesheets/pages.css`: 页面级布局与文案块 / page-level layout and content sections
- `docs/javascripts/reveal.js`: 滚动显现脚本 / reveal-on-scroll script
- `docs/javascripts/theme-toggle.js`: 主题切换与本地存储 / theme toggle and local persistence

## 最近的站点调整 | Recent Site Changes

这一轮不是继续往首页塞内容，而是做减法。
This round was about subtraction rather than adding more sections to the homepage.

主要变化：
Main changes:

- 删掉了多余的解释区、平台结构展示和装饰性背景块。
- Removed extra explainer sections, platform showcase blocks, and decorative background areas.
- 首页改成更像个人博客入口的表达，只保留标题、短句和三个核心入口。
- The homepage now reads more like a personal blog landing page, keeping only the title, a short line, and three core entry points.
- 云盘页改成简洁公开说明，不再把文档页做成服务界面的替身。
- The cloud-drive page now uses concise public-facing notes instead of mimicking the service UI.
- 增加了昼夜主题切换，并让文字、按钮、卡片和边框一起跟随主题变化。
- Added a day-night theme toggle so text, buttons, cards, and borders all follow the selected theme.

## 模块化约束 | Modularity Rules

- 主题颜色、表面层级和边框变量统一放在 `tokens.css`。
- Theme colors, surfaces, and border variables stay in `tokens.css`.
- 通用组件样式放在 `components.css`，避免在页面文件重复定义。
- Shared component styles belong in `components.css` to avoid duplication across pages.
- 页面专属布局和文案块样式放在 `pages.css`。
- Page-specific layout and copy blocks belong in `pages.css`.
- 行为脚本独立维护，不把交互逻辑写进 markdown 内容里。
- Behavior scripts are maintained separately instead of embedding interaction logic into markdown content.

## 注释原则 | Commenting Rules

- 注释用于说明模块职责、状态切换逻辑和不直观的实现原因。
- Comments should explain module responsibility, state transitions, and non-obvious implementation choices.
- 不给显而易见的样式或语法写废话注释。
- Do not add noise comments for obvious syntax or self-explanatory declarations.

## 常用命令 | Common Commands

```bash
python cloud_drive_server.py --host 127.0.0.1 --port 8787
python cloud_gateway.py --host 127.0.0.1 --port 8080
python -m unittest discover -s tests
python -m mkdocs build
```

```bash
sudo systemctl status cloud-drive.service --no-pager
sudo systemctl status caddy.service --no-pager
sudo systemctl status cloud-gateway.service --no-pager
curl -I https://clouddrive.ccwu.cc/
curl https://clouddrive.ccwu.cc/health
```

## 更新记录 | Update Log

### 2026-04-11

- 整合了旧版 README 中仍然有价值的部署说明、状态记录和项目边界说明。
- Merged back the still-useful deployment notes, status records, and project-boundary notes from the previous README.
- 文档站文案改成更简洁的中英双语，并统一成对外展示口径。
- Simplified the docs copy into concise bilingual language with a public-facing tone.
- 首页与云盘页删掉多余部分，重新组织为更像个人站的结构。
- Removed extra sections from the homepage and cloud-drive page and reorganized them into a more personal-site structure.
- 前端继续按模块拆分，并加入主题切换脚本。
- Kept the front end modular and added a dedicated theme-toggle script.
