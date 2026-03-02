@echo off
chcp 65001 >nul 2>&1
echo ============== Grid Map Path 项目启动中 ==============

:: 步骤1：检查Anaconda是否可用
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Anaconda，请先安装并配置环境变量
    pause
    exit /b 1
)

:: 步骤2：创建/激活虚拟环境
conda activate py311_env >nul 2>&1
if %errorlevel% neq 0 (
    echo 未找到py311_env环境，正在创建（需等待1-2分钟）...
    conda create -n py311_env python=3.11 -y >nul 2>&1
    conda activate py311_env >nul 2>&1
)

:: 步骤3：定位项目目录（自动获取当前脚本所在路径）
cd /d "%~dp0"
set PROJECT_PATH=%cd%

:: 步骤4：安装依赖
echo 正在安装/更新依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple >nul 2>&1
if %errorlevel% neq 0 (
    echo 依赖安装失败，请检查网络后重试
    pause
    exit /b 1
)

:: 步骤5：启动项目并打开浏览器
echo 项目启动中...
start http://127.0.0.1:7860
python main.py

echo ============== 启动完成，浏览器已打开 ==============
pause