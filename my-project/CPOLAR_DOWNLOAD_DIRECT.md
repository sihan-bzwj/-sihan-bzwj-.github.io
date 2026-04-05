# Azure VM 上直接安装 Cpolar - 本地下载 + 管道传输方式

## 方式：本地下载 → 通过 SSH 管道直接上传并解压

这个方法不需要在本地保存文件，直接从下载流传输到 VM。

### 前提条件
- 本地有 curl（Windows 已内置 PowerShell）
- SSH 连接正常

### 快速命令

在 **PowerShell** 中运行：

```powershell
# 直接从 Cpolar 官网下载并通过 SSH 管道传输到 VM，自动解压到 /home/azureuser/bin/

curl.exe -L https://www.cpolar.com/static/downloads/cpolar-linux-amd64.tar.gz | `
ssh.exe -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 `
"mkdir -p /home/azureuser/bin && cd /home/azureuser/bin && tar xzf - && chmod +x cpolar && ./cpolar -v"
```

#### 说明：
- `curl.exe -L ...` - 下载 Cpolar（带重定向）
- `|` - 管道符，直接将下载的内容传输给下一条命令
- `ssh ... tar xzf -` - 在 VM 上直接解压（`-` 表示从标准输入读取）
- `chmod +x cpolar` - 设置可执行权限
- `./cpolar -v` - 验证安装成功

### 预期输出
如果成功，会看到 Cpolar 版本号：
```
Version: v3.x.x
```

---

## 如果上述命令失败

### 方案 B：分步操作

#### 1. 本地下载到临时位置
```powershell
# 下载
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri https://www.cpolar.com/static/downloads/cpolar-linux-amd64.tar.gz `
    -OutFile $env:TEMP\cpolar.tar.gz

# 验证
Get-Item $env:TEMP\cpolar.tar.gz | Select-Object -Property FullName, Length
```

#### 2. 通过 SCP 上传（速度快）
```powershell
scp.exe -i C:\Users\jh\.ssh\vm_key.pem `
    $env:TEMP\cpolar.tar.gz `
    azureuser@20.196.193.8:/home/azureuser/bin/cpolar.tar.gz
```

#### 3. 在 VM 上解压
```powershell
ssh.exe -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 `
    "cd /home/azureuser/bin && tar xzf cpolar.tar.gz && chmod +x cpolar && ./cpolar -v"
```

---

## 关键点

- ✅ **优先用方案 A（管道传输）** - 最简洁，无需本地文件
- ✅ **如果方案 A 超时** - 用方案 B 分步操作
- ✅ **验证成功** - 看到版本号就代表安装成功

---

## 验证安装

安装完成后，验证 Cpolar 正常工作：

```powershell
ssh.exe -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 `
    "/home/azureuser/bin/cpolar -version"
```

或直接启动隧道测试：

```powershell
ssh.exe -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 `
    "/home/azureuser/bin/cpolar http 3210 -authtoken cdec8507-3ce7-40a1-9be2-d2406c3cfaae -region cn"
```

如看到隧道地址，说明一切正常。

---

## 然后部署 systemd 服务

一旦 Cpolar 二进制在 `/home/azureuser/bin/cpolar`，就可以运行之前的部署脚本：

```powershell
ssh.exe -i C:\Users\jh\.ssh\vm_key.pem azureuser@20.196.193.8 `
    "bash -s" < C:\Users\jh\Desktop\code\github.io\my-project\deploy-cpolar.sh
```

