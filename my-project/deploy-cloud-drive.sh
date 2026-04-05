#!/bin/bash
# Cloud Drive systemd 部署脚本
# 在 Azure VM 上执行此脚本来安装和启动云盘服务

set -e

echo "=== Cloud Drive systemd 部署脚本 ==="
echo ""

if [ ! -f "/home/azureuser/bin/cloud_drive_server.py" ]; then
    echo "❌ 错误：/home/azureuser/bin/cloud_drive_server.py 不存在"
    echo ""
    echo "请先把 cloud_drive_server.py 上传到 /home/azureuser/bin/"
    echo "例如："
    echo "  scp -i ~/.ssh/vm_key.pem ./cloud_drive_server.py azureuser@20.196.193.8:/home/azureuser/bin/"
    exit 1
fi

chmod +x /home/azureuser/bin/cloud_drive_server.py

echo "确保云盘存储目录存在..."
mkdir -p /home/azureuser/cloud-drive

echo "验证 Python 脚本语法..."
/usr/bin/python3 -m py_compile /home/azureuser/bin/cloud_drive_server.py

echo "安装 cloud-drive.service..."
sudo tee /etc/systemd/system/cloud-drive.service > /dev/null << 'EOF'
[Unit]
Description=Cloud Drive API
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser
Environment="CLOUD_DRIVE_ROOT=/home/azureuser/cloud-drive"
ExecStart=/usr/bin/python3 /home/azureuser/bin/cloud_drive_server.py --host 127.0.0.1 --port 8787 --root /home/azureuser/cloud-drive
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=cloud-drive

[Install]
WantedBy=multi-user.target
EOF

echo "安装 cloud-drive-tunnel.service..."
sudo tee /etc/systemd/system/cloud-drive-tunnel.service > /dev/null << 'EOF'
[Unit]
Description=Cloud Drive Cloudflared Tunnel
After=network-online.target cloud-drive.service
Wants=network-online.target cloud-drive.service

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser
ExecStart=/home/azureuser/cloudflared-linux-amd64 tunnel --url http://127.0.0.1:8787
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=cloud-drive-tunnel

[Install]
WantedBy=multi-user.target
EOF

echo "重新加载 systemd 配置..."
sudo systemctl daemon-reload

echo "启用云盘服务开机自启..."
sudo systemctl enable cloud-drive.service
sudo systemctl enable cloud-drive-tunnel.service

echo "启动云盘 API..."
sudo systemctl restart cloud-drive.service

echo "启动云盘隧道..."
sudo systemctl restart cloud-drive-tunnel.service

echo ""
echo "=== 服务状态 ==="
sleep 2
sudo systemctl status cloud-drive.service --no-pager || true
echo ""
sudo systemctl status cloud-drive-tunnel.service --no-pager || true

echo ""
echo "=== 云盘隧道日志 ==="
echo "运行下面的命令查看公网地址："
echo "  sudo journalctl -u cloud-drive-tunnel -f"
echo ""
echo "或查看最近日志："
echo "  sudo journalctl -u cloud-drive-tunnel -n 50"
echo ""
echo "✅ 部署完成"