#!/bin/bash
# 部署脚本：更新网关并启动访客计数服务
# 在 Azure VM 上执行此脚本

set -e  # 发生错误时停止

echo "═══════════════════════════════════════════════════"
echo "   云网关部署脚本 - IP 访客计数系统启用"
echo "═══════════════════════════════════════════════════"
echo ""

# 检查是否以 azureuser 运行
if [ "$USER" != "azureuser" ]; then
    echo "⚠️  请用 azureuser 账户运行此脚本"
    echo "   或使用: sudo su - azureuser"
    exit 1
fi

# 变量定义
WORK_DIR="/home/azureuser"
GATEWAY_FILE="/home/azureuser/bin/cloud_gateway.py"
SERVICE_FILE="/etc/systemd/system/cloud-gateway.service"
SITE_DIR="$WORK_DIR/site"

echo "📋 部署检查清单..."
echo ""

# 1. 检查 site 目录是否存在
if [ ! -d "$SITE_DIR" ]; then
    echo "❌ 错误：$SITE_DIR 目录不存在"
    echo "   请先从本地上传 site/ 目录"
    exit 1
fi
echo "✅ site 目录已存在"

# 2. 检查 cloud_gateway.py 是否存在
if [ ! -f "$GATEWAY_FILE" ]; then
    echo "❌ 错误：$GATEWAY_FILE 不存在"
    echo "   请先从本地上传新的 cloud_gateway.py"
    exit 1
fi
echo "✅ cloud_gateway.py 已就位"

# 3. 检查 systemd 服务
if [ ! -f "$SERVICE_FILE" ]; then
    echo "❌ 错误：$SERVICE_FILE 服务文件不存在"
    exit 1
fi
echo "✅ systemd 服务配置存在"

echo ""
echo "📦 部署步骤..."
echo ""

# 4. 停止旧的网关服务
echo "⏹️  停止 cloud-gateway 服务..."
sudo systemctl stop cloud-gateway.service 2>/dev/null || true

# 5. 确保新 site 目录有正确的权限
echo "🔐 设置权限..."
sudo chown -R azureuser:azureuser "$SITE_DIR"
chmod 755 "$SITE_DIR"
cd "$SITE_DIR" && find . -type f -exec chmod 644 {} \;

# 6. 验证 index.html 存在
if [ ! -f "$SITE_DIR/index.html" ]; then
    echo "⚠️  警告：$SITE_DIR/index.html 不存在"
    echo "   网站可能无法正常显示"
fi
echo "✅ site 目录权限已设置"

# 7. 重新加载 systemd 配置
echo "🔄 重新加载 systemd 配置..."
sudo systemctl daemon-reload

# 8. 启动网关服务
echo "▶️  启动 cloud-gateway 服务..."
sudo systemctl start cloud-gateway.service

# 9. 检查服务状态
sleep 2
if sudo systemctl is-active --quiet cloud-gateway.service; then
    echo "✅ cloud-gateway 服务已启动"
else
    echo "❌ cloud-gateway 服务启动失败"
    echo "   查看日志: sudo journalctl -u cloud-gateway -n 50"
    exit 1
fi

# 10. 显示服务日志
echo ""
echo "📊 最近日志（10 行）："
echo "═══════════════════════════════════════════════════"
sudo journalctl -u cloud-gateway -n 10 --no-pager
echo "═══════════════════════════════════════════════════"

# 11. 显示验证信息
echo ""
echo "✨ 部署完成！"
echo ""
echo "📍 访问点："
echo "   • Cloudflare 隧道：https://procurement-trying-beside-beginning.trycloudflare.com/"
echo "   • GitHub Pages：https://sihan-bzwj.github.io/-sihan-bzwj-.github.io/"
echo ""
echo "🔍 数据文件："
echo "   • 访客列表：$WORK_DIR/.visitor_ips"
echo "   • 网站内容：$SITE_DIR"
echo ""
echo "📝 日志查看："
echo "   • 实时日志：sudo journalctl -u cloud-gateway -f"
echo "   • 历史日志：sudo journalctl -u cloud-gateway -n 100"
echo ""
echo "🛠️  服务管理："
echo "   • 重启：sudo systemctl restart cloud-gateway.service"
echo "   • 停止：sudo systemctl stop cloud-gateway.service"
echo "   • 状态：sudo systemctl status cloud-gateway.service"
echo "═══════════════════════════════════════════════════"
