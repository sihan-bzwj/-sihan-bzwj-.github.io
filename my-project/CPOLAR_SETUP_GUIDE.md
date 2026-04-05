# Cpolar 国内隧道配置指南

## 快速开始

### 第 1 步：安装 Cpolar
1. 访问 https://www.cpolar.com/download
2. 下载 **Windows 版本** (cpolar-x.x.x-windows-amd64.zip)
3. 解压到 `C:\Program Files\cpolar\` 或任意位置
4. 确保 `cpolar.exe` 可以从命令行运行

### 第 2 步：认证你的 Cpolar 账户
使用提供的 Token 进行认证：

```bash
cpolar authtoken cdec8507-3ce7-40a1-9be2-d2406c3cfaae
```

### 第 3 步：端口转发（重要！）
因为 LobeChat 运行在远程 Azure VM，需要先建立 SSH 端口转发：

**打开一个 PowerShell 终端，运行：**

```powershell
ssh -i C:\Users\jh\.ssh\vm_key.pem -L 3210:127.0.0.1:3210 azureuser@20.196.193.8
```

这样会把 Azure VM 上的 3210 端口映射到本地 127.0.0.1:3210

### 第 4 步：启动 Cpolar 隧道
**打开另一个 PowerShell 终端，运行：**

```bash
cpolar http 3210
```

你会看到类似的输出：
```
Session Status                online
Account                       XXXXXXX
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxxx-xxxxx.cpolar.io -> http://127.0.0.1:3210
```

**记住 `Forwarding` 后面的地址**，这就是你的国内公网地址！

### 第 5 步：访问 LobeChat
在浏览器中访问上面获得的地址，例如：
```
https://xxxxx-xxxxx.cpolar.io
```

---

## 完整流程（脚本化）

或者直接运行预制脚本：

```batch
start-cpolar-tunnel.bat
```

但需要先完成 SSH 端口转发的第 3 步。

---

## 对比：Cloudflare vs Cpolar

| 特性 | Cloudflare Quick Tunnel | Cpolar 国内隧道 |
|------|------------------------|-----------------|
| **延迟** | 国际线路，100-300ms | 国内线路，10-50ms |
| **稳定性** | 很好 | 很好 |
| **免费额度** | 无限 | 有（月限流量，够用） |
| **配置难度** | 低 | 低 |
| **推荐场景** | 国际访问 | 国内用户，需要快速 |

---

## 常见问题

**Q: 已有 Cloudflare 地址，还需要 Cpolar 吗？**  
A: 不是必须的。如果你的用户主要在国内，Cpolar 会快 5-10 倍。

**Q: 可以同时运行两个隧道吗？**  
A: 可以！分别在不同终端运行两个命令。

**Q: 如果隧道断掉了？**  
A: 按 Ctrl+C 停止，重新运行命令即可。

**Q: 怎样让 Cpolar 在后台持续运行？**  
A: 将其配置为 Windows 服务（见高级配置）。

---

## ⚠️ 重要说明：关于运行方式

**Cpolar 需要持续运行**才能保持公网地址有效：
- 如果在本地 Windows 电脑运行 → 电脑关闭后地址失效
- 如果在 Azure VM 运行 → 24/7 可用

**当前已有 24/7 可用的方案**：

### ✅ Cloudflare（推荐用于 24/7 访问）
- **地址**: https://raised-telling-ppm-notre.trycloudflare.com
- **运行模式**: Azure VM 上的 systemd 服务，持续运行
- **延迟**: 国际线路，100-300ms
- **可用性**: ✅ 24/7，无需任何操作

### ⚠️ Cpolar（如果需要国内快速）
- **需要条件**: 持续运行进程（本地/VPS/VM）
- **延迟**: 国内线路，10-50ms（快 5-10 倍）
- **模式**:
  - 本地运行 = 电脑开着时有效
  - VM 运行 = 24/7 可用（但需安装困难）

---

## 当前配置信息

- **Cpolar Token**: `cdec8507-3ce7-40a1-9be2-d2406c3cfaae`（可选，已获得）
- **✅ 默认使用（已配置，24/7 可用）**: https://raised-telling-ppm-notre.trycloudflare.com
- **🔄 备选（需运行进程）**: Cpolar 国内地址（按上述步骤启动）
- **LobeChat 本地地址**: http://localhost:3210 （SSH 转发后）
- **Azure VM**: 20.196.193.8:3210

---

## 高级配置：Windows 服务（可选）

如果想让 Cpolar 开机自启，可以用 NSSM（Non-Sucking Service Manager）包装成 Windows 服务。

