# 🚀 Azure VM 完整部署指南
# IP: 20.196.193.8
# 用户: azureuser

## 第一步：从本地连接到 Azure VM

在本地 PowerShell 执行：

```powershell
# 检查密钥文件权限
ls ~\myKey.pem

# SSH 连接到 Azure VM
ssh -i ~/myKey.pem azureuser@20.196.193.8
```

## 第二步：在 Azure VM 上执行部署（一行一行复制粘贴）

### 2.1 更新代码
```bash
cd /home/azureuser/repo
git pull origin main
```

### 2.2 备份旧文件
```bash
mkdir -p /home/azureuser/backup
cp /home/azureuser/bin/cloud_gateway.py /home/azureuser/backup/ 2>/dev/null || true
[ -d /home/azureuser/site ] && cp -r /home/azureuser/site /home/azureuser/backup/site_old 2>/dev/null || true
```

### 2.3 部署网关
```bash
cp /home/azureuser/repo/my-project/cloud_gateway.py /home/azureuser/bin/
chmod 755 /home/azureuser/bin/cloud_gateway.py
echo "✅ 网关已更新"
```

### 2.4 部署网站
```bash
rm -rf /home/azureuser/site
cp -r /home/azureuser/repo/my-project/site /home/azureuser/
chown -R azureuser:azureuser /home/azureuser/site
chmod 755 /home/azureuser/site
find /home/azureuser/site -type f -exec chmod 644 {} \;
echo "✅ 网站已部署"
```

### 2.5 更新 systemd 服务
```bash
sudo cp /home/azureuser/repo/my-project/cloud-gateway.service /etc/systemd/system/
sudo systemctl daemon-reload
echo "✅ systemd 已更新"
```

### 2.6 重启网关服务
```bash
sudo systemctl stop cloud-gateway.service 2>/dev/null || true
sudo systemctl start cloud-gateway.service
sleep 3
sudo systemctl status cloud-gateway.service
```

## 第三步：验证部署

### 3.1 检查服务状态
```bash
sudo systemctl is-active cloud-gateway.service && echo "✅ 服务运行中" || echo "❌ 服务未启动"
```

### 3.2 测试 API 端点
```bash
curl http://localhost:8080/api/visitor-count | python3 -m json.tool
```
应该看到：`{"count": N, "success": true}`

### 3.3 测试网站访问
```bash
curl http://localhost:8080/ | head -20
```
应该看到 HTML 内容

### 3.4 查看日志
```bash
sudo journalctl -u cloud-gateway -n 10
```

## 第四步：验证外部访问（可选）

在本地浏览器访问：
- Cloudflare 隧道: https://procurement-trying-beside-beginning.trycloudflare.com/
- LobeChat: https://procurement-trying-beside-beginning.trycloudflare.com
- 云盘: https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive

## 常用命令

```bash
# 查看服务状态
sudo systemctl status cloud-gateway.service

# 查看实时日志
sudo journalctl -u cloud-gateway -f

# 查看历史日志（最近 30 行）
sudo journalctl -u cloud-gateway -n 30

# 重启服务
sudo systemctl restart cloud-gateway.service

# 停止服务
sudo systemctl stop cloud-gateway.service

# 查看访客数据
cat /home/azureuser/.visitor_ips | wc -l

# 查看网站文件列表
ls -la /home/azureuser/site/
```

## 故障排查

### 问题：服务无法启动
```bash
# 查看详细错误
sudo journalctl -u cloud-gateway -n 50
# 检查网关权限
ls -la /home/azureuser/bin/cloud_gateway.py
# 检查 site 目录
ls -la /home/azureuser/site/index.html
```

### 问题：访客计数显示"加载中"
```bash
# 确认 API 响应
curl -v http://localhost:8080/api/visitor-count
# 查看 CORS 头
curl -I http://localhost:8080/api/visitor-count
```

### 问题：网站返回 404
```bash
# 检查文件是否存在
test -f /home/azureuser/site/index.html && echo "✅ index.html 存在" || echo "❌ 不存在"
# 检查权限
ls -la /home/azureuser/site/
```

## 💾 恢复备份（如出现问题）

```bash
# 恢复网关
cp /home/azureuser/backup/cloud_gateway.py /home/azureuser/bin/

# 恢复网站
rm -rf /home/azureuser/site
cp -r /home/azureuser/backup/site_old /home/azureuser/site

# 重启服务
sudo systemctl restart cloud-gateway.service
```

---

**⏱️ 预计部署时间**：10-15 分钟  
**✅ 成功标志**：访问 Cloudflare 隧道网站，页脚显示访客数字（不是"加载中"）
