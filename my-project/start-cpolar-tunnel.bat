@echo off
REM Cpolar 启动脚本 - 用于连接到 LobeChat
REM Token: cdec8507-3ce7-40a1-9be2-d2406c3cfaae

REM 检查 cpolar.exe 是否存在
if not exist "C:\Program Files\cpolar\cpolar.exe" (
    echo Cpolar 未安装，请先从 https://www.cpolar.com/download 下载并安装
    pause
    exit /b 1
)

REM 启动 Cpolar，连接到本地 LobeChat 服务（3210 端口）
echo 正在启动 Cpolar 隧道...
echo Token: cdec8507-3ce7-40a1-9be2-d2406c3cfaae
echo 如配置无误，会显示公网地址...

"C:\Program Files\cpolar\cpolar.exe" authtoken cdec8507-3ce7-40a1-9be2-d2406c3cfaae

REM 等待用户输入后再启动隧道
echo.
echo 认证完成，按 Enter 启动隧道...
pause

REM 注意：这里假设 Azure VM 的 LobeChat 在本地 3210 端口可访问
REM 如果 LobeChat 在远程 VM，需要先通过 SSH 做端口转发：
REM ssh -i C:\Users\jh\.ssh\vm_key.pem -L 3210:127.0.0.1:3210 azureuser@20.196.193.8

echo 启动 HTTP 隧道到 localhost:3210
"C:\Program Files\cpolar\cpolar.exe" http 3210

pause
