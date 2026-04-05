# 更新日志

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
