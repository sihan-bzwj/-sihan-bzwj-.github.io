#!/bin/bash
# 一键部署脚本 - 直接在 Azure VM 的 Terminal 中运行此脚本
# 使用方法：
# 1. 从 GitHub clone 最新代码
# 2. 复制以下命令到 Azure VM Terminal 中
# 3. 按 Enter 执行

# ============================================================
# 快速部署：更新网关并启用访客计数
# ============================================================

set -e

echo "🚀 开始部署云网关..." 

# 定义变量
REPO_DIR="/home/azureuser/repo"
WORK_DIR="/home/azureuser"
GATEWAY_BIN="/home/azureuser/bin"

# 检查 repo 目录
if [ ! -d "$REPO_DIR" ]; then
    echo "❌ 错误：找不到 $REPO_DIR"
    echo "   请先 git clone 项目到此目录"
    exit 1
fi

echo "✅ 找到项目目录"

# 1. 备份旧文件
echo "💾 备份旧文件..."
if [ -f "$GATEWAY_BIN/cloud_gateway.py" ]; then
    cp "$GATEWAY_BIN/cloud_gateway.py" "$GATEWAY_BIN/cloud_gateway.py.bak"
    echo "✅ 已备份 cloud_gateway.py"
fi

# 2. 更新网关
echo "📝 更新 cloud_gateway.py..."
cp "$REPO_DIR/my-project/cloud_gateway.py" "$GATEWAY_BIN/cloud_gateway.py"
chmod 755 "$GATEWAY_BIN/cloud_gateway.py"
echo "✅ cloud_gateway.py 已更新"

# 3. 更新网站文件
echo "📁 更新网站文件..."
rm -rf "$WORK_DIR/site.bak" 2>/dev/null || true
if [ -d "$WORK_DIR/site" ]; then
    mv "$WORK_DIR/site" "$WORK_DIR/site.bak"
    echo "✅ 已备份旧 site 目录"
fi

cp -r "$REPO_DIR/my-project/site" "$WORK_DIR/site"
chown -R azureuser:azureuser "$WORK_DIR/site"
chmod 755 "$WORK_DIR/site"
find "$WORK_DIR/site" -type f -exec chmod 644 {} \;
echo "✅ 网站文件已更新"

# 4. 更新 systemd 服务（如需要）
if grep -q "site-dir" "/etc/systemd/system/cloud-gateway.service"; then
    echo "✅ systemd 服务已配置好 site-dir 参数"
else
    echo "⚠️  正在更新 systemd 服务..."
    sudo cp "$REPO_DIR/my-project/cloud-gateway.service" /etc/systemd/system/
    sudo systemctl daemon-reload
    echo "✅ systemd 服务已更新"
fi

# 5. 重启服务
echo "🔄 重启 cloud-gateway 服务..."
sudo systemctl restart cloud-gateway.service
sleep 2

# 6. 验证服务状态
if sudo systemctl is-active --quiet cloud-gateway.service; then
    echo "✅ 服务已启动"
else
    echo "❌ 服务启动失败，查看日志..."
    sudo journalctl -u cloud-gateway -n 20
    exit 1
fi

# 7. 显示部署完成信息
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║           ✨ 部署完成！                             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📊 部署摘要："
echo "   • 网关：已更新（支持网站 + API）"
echo "   • 网站：已部署"
echo "   • 访客计数：已启用"
echo ""
echo "📍 访问地址："
echo "   • Cloudflare: https://procurement-trying-beside-beginning.trycloudflare.com/"
echo "   • LobeChat:   https://procurement-trying-beside-beginning.trycloudflare.com"
echo "   • 云盘:       https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive"
echo ""
echo "✅ 测试 API："
echo "   curl http://localhost:8080/api/visitor-count"
echo ""
echo "📝 查看日志："
echo "   sudo journalctl -u cloud-gateway -f"
echo ""
echo "🔧 其他命令："
echo "   • 重启: sudo systemctl restart cloud-gateway.service"
echo "   • 停止: sudo systemctl stop cloud-gateway.service"
echo "   • 状态: sudo systemctl status cloud-gateway.service"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""
