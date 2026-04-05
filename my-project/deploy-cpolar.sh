#!/bin/bash
# Cpolar systemd 服务部署脚本
# 在 Azure VM 上执行此脚本来安装和启动 Cpolar 服务

set -e

echo "=== Cpolar systemd 部署脚本 ==="
echo ""

# 检查 cpolar 二进制是否存在
if [ ! -f "/home/azureuser/bin/cpolar" ]; then
    echo "❌ 错误：/home/azureuser/bin/cpolar 不存在"
    echo ""
    echo "请先下载 Cpolar 二进制："
    echo "1. 访问 https://www.cpolar.com/download"
    echo "2. 下载 Linux x64 版本"
    echo "3. 解压并上传到 /home/azureuser/bin/cpolar"
    echo ""
    echo "或者使用 SCP 上传："
    echo "  scp -i ~/.ssh/vm_key.pem /path/to/cpolar azureuser@20.196.193.8:/home/azureuser/bin/"
    exit 1
fi

# 检查权限
if [ ! -x "/home/azureuser/bin/cpolar" ]; then
    echo "设置 cpolar 为可执行..."
    chmod +x /home/azureuser/bin/cpolar
fi

# 验证 cpolar 正常
echo "验证 Cpolar 版本..."
/home/azureuser/bin/cpolar -v || {
    echo "❌ cpolar 验证失败"
    exit 1
}

echo "✅ Cpolar 二进制检查通过"
echo ""

# 复制 systemd 服务文件
echo "安装 systemd 服务文件..."
sudo tee /etc/systemd/system/cpolar.service > /dev/null << 'EOF'
[Unit]
Description=Cpolar HTTP Tunnel for LobeChat
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/azureuser/bin/cpolar http 3210 -authtoken cdec8507-3ce7-40a1-9be2-d2406c3cfaae -region cn
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=cpolar

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd
echo "重新加载 systemd 配置..."
sudo systemctl daemon-reload

# 启用服务开机自启
echo "启用 cpolar 服务开机自启..."
sudo systemctl enable cpolar.service

# 启动服务
echo "启动 cpolar 服务..."
sudo systemctl start cpolar.service

# 检查状态
echo ""
echo "=== 服务状态 ==="
sleep 2
sudo systemctl status cpolar.service --no-pager || true

echo ""
echo "=== 查看实时日志 ==="
echo "运行以下命令查看 Cpolar 隧道地址："
echo "  sudo journalctl -u cpolar -f"
echo ""
echo "或查看最近的日志："
echo "  sudo journalctl -u cpolar -n 50"
echo ""
echo "✅ 部署完成！Cpolar 现在作为 systemd 服务运行"
echo "   - 自动开机启动"
echo "   - 异常停止时自动重启"
echo "   - 日志记录在 systemd journal 中"
