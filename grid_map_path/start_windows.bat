@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

echo ===== Grid Map Path =====
where python >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Python。请安装 Python 3.11 或更高版本并加入 PATH。
    pause
    exit /b 1
)

echo 正在安装或检查依赖...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo 错误：依赖安装失败。
    pause
    exit /b 1
)

echo 正在启动应用，请稍候...
python main.py
if errorlevel 1 (
    echo 应用异常退出。
    pause
    exit /b 1
)
endlocal
