# GitHub Pages 公网站点部署指南

## 📍 访问地址

```
https://sihan-bzwj.github.io/
```

**注意**：标准用户主页仓库名称应为 `sihan-bzwj.github.io`。

---

## ✅ 已完成的工作

1. ✅ **部署到 gh-pages 分支**
   - 使用 `mkdocs gh-deploy --force` 命令
   - 最新网站文件已推送到 GitHub

2. ✅ **添加 site_url 配置**
   - mkdocs.yml 中已添加 `site_url: https://sihan-bzwj.github.io/`
   - 确保所有资源路径正确

3. ✅ **工作流配置**
   - .github/workflows/deploy.yml 已创建
   - 每次推送到 main 分支时自动部署

---

## 🔧 故障排查

### 1️⃣ 页面仍不显示？

**可能原因**：GitHub 缓存延迟（通常 5-10 分钟）

**解决方案**：
- 等待 5-10 分钟后刷新
- 强制刷新：`Ctrl + Shift + R` (Windows) 或 `Cmd + Shift + R` (Mac)
- 清除浏览器缓存或在隐私模式打开

### 2️⃣ 检查 GitHub Pages 设置

进入仓库的 **Settings** → **Pages**：

1. **检查发布源**：
   - Source 应该是 `Deploy from a branch`
   - Branch 应该是 `gh-pages` 和 `/(root)`

2. **检查自定义域名**（可选）：
   - 如果需要自定义域名，在此处配置
   - 将生成 CNAME 文件

### 3️⃣ 验证 gh-pages 分支内容

```bash
# 查看 gh-pages 分支是否有文件
git show gh-pages:index.html | head -10

# 应该看到 Material for MkDocs 格式的 HTML：
# <!doctype html>
# <html lang="zh" class="no-js">
```

### 4️⃣ 检查 GitHub Actions 部署状态

1. 进入仓库 **Actions** 标签
2. 查看最新的 "Deploy MkDocs site" 工作流
3. 如果显示 ✅ (绿色)，部署成功
4. 如果显示 ❌ (红色)，点击查看错误

---

## 📊 访问途径

| 方式 | 地址 | 说明 |
|------|------|------|
| GitHub Pages | https://sihan-bzwj.github.io/ | 公网 GitHub 部署 |
| Azure VM | https://procurement-trying-beside-beginning.trycloudflare.com/ | Cloudflare 隧道 |
| 本地测试 | http://localhost:8080 | 本地网关服务 |

---

## 🔄 更新网站流程

### 方式 1: 自动部署（推荐）

```bash
# 编辑文档
vim my-project/docs/index.md

# 提交并推送到 main 分支
git add -A
git commit -m "Update content"
git push origin main

# GitHub Actions 会自动部署到 GitHub Pages
```

### 方式 2: 手动部署

```bash
cd my-project
mkdocs gh-deploy --force
```

---

## 🎯 常见问题

**Q: 为什么要用这个短 URL？**  
A: 因为仓库名称使用标准格式 `username.github.io` 后，主页会直接发布在 `https://username.github.io`。

**Q: 页面显示乱码****Q: 页面显示乱码？**  
A: MkDocs 会自动处理编码。检查 mkdocs.yml 中的 language 设置是否为 `zh`

**Q: CORS 报错？**  
A: 这是浏览器安全限制。GitHub Pages 上的 JavaScript 无法直接调用 Azure VM API。
- 解决方案：在 API 服务器添加 CORS 头（已在 cloud_gateway.py 中实现）

---

## 📝 部署历史

| 日期 | 操作 | commit |
|------|------|--------|
| 2026-04-05 | 手动部署网站 | 8c856eb |
| 2026-04-05 | 添加 site_url | 62279c2 |
| 2026-04-05 | 添加 site_url config | 1351c84 |

---

## 💡 下一步建议

1. **验证 GitHub Pages 显示** → 检查 Settings > Pages
2. **如果需要自定义域名** → 进行 DNS 配置
3. **如果希望整合访客计数** → 在 GitHub Actions 中调用 Azure VM API
4. **持续更新文档** → push 到 main，自动部署

---

**最后更新**：2026-04-05  
**维护人员**：Sihan
