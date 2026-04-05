# 部署检查清单

## 📋 必需的文件

在 Azure VM 的以下位置需要更新：

```
/home/azureuser/
├── bin/
│   └── cloud_gateway.py          ← 新版本（已更新，支持网站服务）
├── site/                          ← 网站目录（需要上传）
│   ├── index.html
│   ├── 404.html
│   ├── sitemap.xml
│   ├── assets/
│   ├── javascripts/
│   │   └── site-footer.js
│   ├── stylesheets/
│   ├── search/
│   └── cloud-drive/
├── .visitor_ips                   ← 自动创建（无需上传）
└── cloud-drive/                   ← 已存在
```

## 🚀 部署步骤

### 步骤 1：在本地验证
```bash
# 在 Windows 本地
cd c:\Users\jh\Desktop\code\github.io\my-project

# 确保 site/ 目录存在
ls site/

# 确保 cloud_gateway.py 最新
ls -la cloud_gateway.py
```

### 步骤 2：上传文件到 Azure VM

使用 SCP 或您喜欢的方法上传：

```bash
# 方式 A：使用 scp 上传（在本地 PowerShell）
scp -r "c:\Users\jh\Desktop\code\github.io\my-project\site" azureuser@<VM_IP>:/home/azureuser/

# 方式 B：使用 Azure 文件上传工具
# 登录 Azure Portal → VM → 上传文件

# 方式 C：使用 git 同步（如果 VM 上有 GitHub 访问权限）
cd /home/azureuser/repo
git pull origin main
```

### 步骤 3：在 Azure VM 上执行部署脚本

```bash
# SSH 连接到 VM
ssh azureuser@<VM_IP>

# 变成 azureuser（如果不是）
sudo su - azureuser

# 下载或创建部署脚本
# （脚本已在项目中：my-project/deploy.sh）

# 执行部署脚本
bash ~/deploy.sh
```

### 步骤 4：验证部署

```bash
# 查看服务状态
sudo systemctl status cloud-gateway.service

# 查看最近的日志
sudo journalctl -u cloud-gateway -n 20

# 测试 API 端点
curl http://localhost:8080/api/visitor-count

# 测试网站访问
curl http://localhost:8080/ | head -20
```

## 🔧 文件清单

| 文件 | 大小 | 更新说明 |
|------|------|---------|
| cloud_gateway.py | ~15KB | **必更新** - 添加网站服务功能 |
| site/ 目录 | ~5MB | **必上传** - MkDocs 生成的静态网站 |
| cloud-gateway.service | ~0.5KB | 已更新参数（--site-dir） |
| deploy.sh | ~3KB | 辅助脚本（可选）|

## ⚠️ 常见问题

### Q: 上传后网站还是显示 404？
A: 检查 site 目录权限
```bash
ls -la /home/azureuser/site/
# 应该显示 index.html
```

### Q: API 返回错误？
A: 检查服务日志
```bash
sudo journalctl -u cloud-gateway -n 50
```

### Q: 访客计数还是显示"加载中"？
A: 
1. 确保 API 正确部署：`curl http://localhost:8080/api/visitor-count`
2. 检查 CORS 头是否返回
3. 查看浏览器控制台错误

### Q: 我不知道 VM 的 IP 地址？
A: 在 Azure Portal 查看 → 虚拟机 → 概览 → 公共 IP 地址

## 📞 需要帮助？

如果部署出现问题，收集以下信息：

```bash
# 1. 服务状态
sudo systemctl status cloud-gateway.service

# 2. 最近日志
sudo journalctl -u cloud-gateway -n 30 > /tmp/log.txt

# 3. API 测试结果
curl -v http://localhost:8080/api/visitor-count

# 4. 文件检查
ls -la /home/azureuser/site/index.html
```

---

**部署预计时间**：5-10 分钟  
**部署日期**：2026-04-05  
**涉及提交**：55d1cfd, ee59dcd
