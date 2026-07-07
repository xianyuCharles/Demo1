@echo off
chcp 65001 >nul
echo ============================================
echo   Demo 1 - 订单数据自动化处理系统 打包工具
echo   星亦网络科技工作室
echo ============================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python环境
    echo 请先安装Python 3.10+：https://www.python.org/downloads/
    echo 安装时请勾选"Add Python to PATH"
    pause
    exit /b 1
)

echo [1/4] 安装打包依赖...
pip install pyinstaller pandas openpyxl jinja2 -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [2/4] 清理旧文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del /q *.spec

echo [3/4] 开始打包（预计1-3分钟）...
pyinstaller --onefile ^
    --name "订单数据处理工具" ^
    --add-data "modules;modules" ^
    --hidden-import pandas ^
    --hidden-import openpyxl ^
    --hidden-import jinja2 ^
    --console ^
    scripts/process.py

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo [4/4] 准备交付包...
if not exist "交付包" mkdir "交付包"
copy /y "dist\订单数据处理工具.exe" "交付包\" >nul
xcopy /e /y /q "input" "交付包\input\" >nul 2>&1
if not exist "交付包\input" mkdir "交付包\input"
if not exist "交付包\output" mkdir "交付包\output"

echo.
echo ============================================
echo   打包完成！
echo ============================================
echo.
echo 交付包位置: 交付包\
echo   - 订单数据处理工具.exe  （主程序）
echo   - input\                （放入CSV文件）
echo   - output\               （结果输出目录）
echo.
echo 使用方法：
echo   1. 将CSV文件放入 input 文件夹
echo   2. 双击运行 订单数据处理工具.exe
echo   3. 查看 output 文件夹中的结果
echo.
pause
