@echo off
:: 1. 激活环境（使用你的conda路径）
call E:\anaconda\condabin\conda.bat activate py311_env
if %errorlevel% neq 0 (
    echo 错误：无法激活py311_env环境，请检查环境名是否正确
    pause
    exit /b 1
)

:: 2. 定位到项目目录
cd /d "E:\the summary of the code\Grid Map Path"
if %errorlevel% neq 0 (
    echo 错误：项目目录不存在，请核对路径
    pause
    exit /b 1
)

:: 3. 安装依赖（如果有requirements.txt）
pip install -r requirements.txt --upgrade
if %errorlevel% neq 0 (
    echo 提示：依赖安装失败，可能是无requirements.txt文件，可忽略此提示继续
)

:: 4. 启动项目（替换为你的入口文件，比如main.py）
python main.py
if %errorlevel% neq 0 (
    echo 错误：启动失败，请检查入口文件是否存在
    pause
    exit /b 1
)

pause