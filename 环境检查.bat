@echo off
chcp 65001 >nul
echo ==============================================
echo       佳明 (Garmin Connect IQ) 开发环境体检
echo ==============================================
echo.

echo [1/5] 检查 Java (JDK 17) 运行环境:
java -version
if %errorlevel% neq 0 (
    echo [!] 警告: 未在当前窗口识别到 java 命令，请重启命令行或检查 PATH。
) else (
    echo [OK] Java 运行环境正常。
)
echo.

echo [2/5] 检查开发者密钥 (developer_key.der):
if exist "d:\Garmin\developer_key.der" (
    echo [OK] 开发者私钥已就绪: d:\Garmin\developer_key.der
) else (
    echo [!] 未检测到 developer_key.der
)
echo.

echo [3/5] 检查 Garmin SDK Manager:
if exist "d:\Garmin\tools\sdkmanager\sdkmanager.exe" (
    echo [OK] SDK 管理器已安装: d:\Garmin\tools\sdkmanager\sdkmanager.exe
) else (
    echo [!] 未找到 SDK 管理器。
)
echo.

echo [4/5] 检查 Connect IQ 已下载 SDK 与设备:
if exist "%APPDATA%\Garmin\ConnectIQ\current-sdk.cfg" (
    echo [OK] 已配置当前 SDK:
    type "%APPDATA%\Garmin\ConnectIQ\current-sdk.cfg"
) else (
    echo [提示] 尚未下载或激活 SDK，请运行 "启动SDK管理器.bat" 下载最新 SDK 并点击 "Use as current SDK"。
)
echo.

echo [5/5] 检查 VS Code Monkey C 插件:
call code --list-extensions | findstr /i "garmin.monkey-c" >nul
if %errorlevel% equ 0 (
    echo [OK] VS Code 官方 Monkey C 插件已安装。
) else (
    echo [!] VS Code Monkey C 插件未安装。
)
echo.
echo ==============================================
pause
