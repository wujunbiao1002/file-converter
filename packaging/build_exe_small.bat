@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo 开始构建Junly文件转换工具轻量版可执行程序...

rem 设置工作目录为项目根目录
cd ..

rem 确认UPX已安装
if not exist ".venv\Lib\site-packages\PyInstaller\utils\upx\upx.exe" (
    echo UPX压缩工具未安装，正在安装...
    call packaging\install_upx.bat
)

rem 激活虚拟环境（如果有）
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

rem 确保安装了必要的工具
pip install -r requirements.txt
pip install pyinstaller

rem 清理旧的构建文件
echo 清理旧的构建文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "src\__pycache__" rmdir /s /q "src\__pycache__"

rem 使用优化的spec文件构建
echo 正在使用稳定版构建选项...
pyinstaller --clean --upx-dir=".venv\Lib\site-packages\PyInstaller\utils\upx" packaging\file_converter.spec

echo.
if %errorlevel% equ 0 (
    echo 构建成功！轻量版可执行文件位于 dist\Junly文件转换工具 目录中
    
    rem 清理构建过程中生成的临时文件
    echo 清理构建临时文件...
    if exist build rmdir /s /q build
    if exist "*.spec" (
        for %%i in (*.spec) do (
            if not "%%i"=="file_converter.spec" del /f /q "%%i"
        )
    )
    
    rem 彻底清理Python缓存文件
    echo 清理Python缓存文件...
    for /d /r . %%d in (__pycache__) do (
        if exist "%%d" (
            echo 删除: %%d
            rmdir /s /q "%%d"
        )
    )
    
    for /d /r . %%d in (*.egg-info) do (
        if exist "%%d" (
            echo 删除: %%d
            rmdir /s /q "%%d"
        )
    )
    
    for /r . %%f in (*.pyc) do (
        if exist "%%f" (
            echo 删除: %%f
            del /f /q "%%f"
        )
    )
    
    rem 清理PyInstaller生成的临时文件
    if exist "warn*.txt" del /f /q "warn*.txt"
    if exist "logdict*.txt" del /f /q "logdict*.txt"
    
    echo 已清理所有临时文件和构建目录
    
    rem 计算打包后的文件大小
    echo 正在计算打包后的文件大小...
    powershell -command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-ChildItem -Path 'dist' -Recurse | Measure-Object -Property Length -Sum | Select-Object @{Name='TotalSize(MB)';Expression={'{0:N2}' -f ($_.Sum / 1MB)}}}"
    
    echo.
    echo 打包和清理完成！
) else (
    echo 构建失败，请检查错误信息
)

rem 如果使用了虚拟环境，停用它
if exist .venv\Scripts\deactivate.bat (
    call .venv\Scripts\deactivate.bat
)

rem 返回到packaging目录
cd packaging

endlocal
pause 