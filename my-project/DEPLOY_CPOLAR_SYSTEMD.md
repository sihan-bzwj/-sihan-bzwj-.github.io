# Azure VM 上部署 Cpolar systemd 服务

## 快速开始（3 步）

### 第 1 步：本地下载 Cpolar
在你的 Windows 电脑上：

1. 访问 https://www.cpolar.com/download
2. 下载 **Linux x64** 版本（.tar.gz 或 .zip）
3. 解压到某个文件夹，获得 `cpolar` 二进制

例如下载后：
```
C:\Users\jh\Downloads\cpolar-linux-amd64\cpolar
```

### 第 2 步：上传 Cpolar 到 Azure VM

在 PowerShell 中运行（替换路径）：

```powershell
# 假设你下载的 cpolar 在 C:\Users\jh\Downloads\cpolar-linux-amd64\cpolar
scp -i C:\Users\jh\.ssh\vm_key.pem `
    C:\Users\jh\Downloads\cpolar-linux-amd64\cpolar `
    azureuser@20.196.193.8:/home/azureuser/bin/cpolar
```

验证上传成功：
```powershell
ssh -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 "ls -lh /home/azureuser/bin/cpolar"
```

应该看到：
```
-rwxr-xr-x 1 azureuser azureuser 12M Apr  4 15:30 /home/azureuser/bin/cpolar
```

### 第 3 步：在 VM 上执行部署脚本

```powershell
ssh -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 "bash -s" < C:\Users\jh\Desktop\code\github.io\my-project\deploy-cpolar.sh
```

或者如果提示权限不足，用 sudo：

```powershell
ssh -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 "sudo bash - " << 'EOF'
# (粘贴 deploy-cpolar.sh 的文件内容)
EOF
```

---

## 手动部署步骤（如果脚本失败）

### 1. 上传 cpolar 二进制
```bash
scp -i ~/.ssh/vm_key.pem /path/to/cpolar azureuser@20.196.193.8:/home/azureuser/bin/
```

### 2. SSH 到 VM
```bash
ssh -i ~/.ssh/vm_key.pem azureuser@20.196.193.8
```

### 3. 设置权限
```bash
chmod +x /home/azureuser/bin/cpolar
```

### 4. 上传 systemd 服务文件
在本地上传 `cpolar.service` 文件：
```bash
scp -i ~/.ssh/vm_key.pem ./cpolar.service azureuser@20.196.193.8:/home/azureuser/
```

### 5. 在 VM 上安装服务
```bash
sudo mv /home/azureuser/cpolar.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cpolar.service
sudo systemctl start cpolar.service
```

### 6. 验证服务
```bash
sudo systemctl status cpolar.service
sudo journalctl -u cpolar -n 50
```

---

## 查看 Cpolar 隧道地址

部署完成后，查看隧道地址：

```bash
ssh -i ~/.ssh/vm_key.pem azureuser@20.196.193.8 "sudo journalctl -u cpolar | grep -i 'forwarding\|tunnel\|http'"
```

或实时查看：
```bash
ssh -i ~/.ssh/vm_key.pem azureuser@20.196.193.8 "sudo journalctl -u cpolar -f"
```

会显示类似：
```
Forwarding    https://xxxxx-xxxxx.cpolar.io -> http://localhost:3210
```

---

## 常见问题

**Q: 无法找到 Cpolar 下载？**
A: 访问 https://www.cpolar.com/download → 选择 Linux x64

**Q: 上传失败 - Permission denied？**
A: 检查 SSH key 权限：
```bash
chmod 600 ~/.ssh/vm_key.pem
```

**Q: 启动失败 - cpolar: command not found？**
A: 检查二进制是否可执行：
```bash
chmod +x /home/azureuser/bin/cpolar
```

**Q: 隧道一直显示?**
A: 等待 5-10 秒，然后查看日志：
```bash
sudo journalctl -u cpolar -n 100
```

**Q: 想停止或重启服务？**
A: 
```bash
sudo systemctl stop cpolar.service      # 停止
sudo systemctl restart cpolar.service   # 重启
sudo systemctl status cpolar.service    # 查看状态
```

---

## 配置说明

当前 systemd 配置：
- **Token**: cdec8507-3ce7-40a1-9be2-d2406c3cfaae
- **Region**: cn （中国）
- **Local Port**: 3210 （LobeChat）
- **Restart**: 自动重启（异常停止时）
- **User**: azureuser
- **Logging**: systemd journal

---

## 部署完成后

✅ **Cpolar 隧道 24/7 运行**，无需任何操作
✅ **访问地址**：https://xxxxx-xxxxx.cpolar.io （部署后会显示）
✅ **对比 Cloudflare**：国内延迟快 5-10 倍

如有问题，查看日志：
```bash
sudo journalctl -u cpolar -f
```

