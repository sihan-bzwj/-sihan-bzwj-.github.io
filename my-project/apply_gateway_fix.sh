#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing gateway and service files..."
sudo install -m 755 "$SCRIPT_DIR/cloud_gateway.py" /home/azureuser/bin/cloud_gateway.py
sudo install -m 644 "$SCRIPT_DIR/cloud-drive.service" /etc/systemd/system/cloud-drive.service
sudo install -m 644 "$SCRIPT_DIR/cloud-gateway.service" /etc/systemd/system/cloud-gateway.service
sudo install -m 644 "$SCRIPT_DIR/cloudflared.service" /etc/systemd/system/cloudflared.service

echo "Reloading systemd and restarting services..."
sudo systemctl daemon-reload
sudo systemctl enable cloud-drive.service
sudo systemctl enable cloud-gateway.service
sudo systemctl enable cloudflared.service
sudo systemctl restart cloud-drive.service
sudo systemctl restart cloud-gateway.service
sudo systemctl restart cloudflared.service

echo "Checking service status..."
sudo systemctl --no-pager --full status cloud-drive.service cloud-gateway.service cloudflared.service

echo "Checking local gateway routes..."
curl -sS -I http://127.0.0.1:8080/ | head -n 1
curl -sS -I http://127.0.0.1:8080/cloud-drive | head -n 1
curl -sS http://127.0.0.1:8080/cloud-drive/health | head -c 300

echo "Done. Validate public URLs in browser:"
echo "  https://procurement-trying-beside-beginning.trycloudflare.com/"
echo "  https://procurement-trying-beside-beginning.trycloudflare.com/cloud-drive"
