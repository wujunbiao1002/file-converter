@echo off
chcp 65001 >nul
echo 开始构建Junly文件转换工具可执行程序...

rem 设置工作目录为项目根目录
cd ..

rem 激活虚拟环境（如果有）
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

rem 确保安装了必要的工具
pip install -r requirements.txt
pip install pyinstaller

rem 清理旧的构建文件
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist "*.spec" (
    for %%i in (*.spec) do (
        if not "%%i"=="file_converter.spec" del /f /q "%%i"
    )
)
if exist __pycache__ rmdir /s /q __pycache__

rem 使用spec文件构建
echo 正在构建标准版...
pyinstaller --clean packaging\file_converter.spec

echo.
if %errorlevel% equ 0 (
    echo 构建成功！可执行文件位于 dist\Junly文件转换工具 目录中
    
    rem 清理构建过程中生成的临时文件
    if exist build rmdir /s /q build
    if exist "*.spec" (
        for %%i in (*.spec) do (
            if not "%%i"=="file_converter.spec" del /f /q "%%i"
        )
    )
    if exist __pycache__ rmdir /s /q __pycache__
    
    rem 清理Python缓存文件
    FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
    FOR /d /r . %%d IN (*.egg-info) DO @IF EXIST "%%d" rd /s /q "%%d"
    FOR /r . %%f IN (*.pyc) DO @IF EXIST "%%f" del /f /q "%%f"
    
    echo 已清理所有临时文件和构建目录
) else (
    echo 构建失败，请检查错误信息
)

rem 如果使用了虚拟环境，停用它
if exist .venv\Scripts\deactivate.bat (
    call .venv\Scripts\deactivate.bat
)

rem 返回到packaging目录
cd packaging

pause 