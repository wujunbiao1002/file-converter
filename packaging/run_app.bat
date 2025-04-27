@echo off
chcp 65001 >nul
echo 正在启动Junly文件转换工具...

rem 设置工作目录为项目根目录
cd ..

if exist "dist\Junly文件转换工具\Junly文件转换工具.exe" (
    start "" "dist\Junly文件转换工具\Junly文件转换工具.exe"
    
    rem 返回到packaging目录
    cd packaging
) else (
    echo 未找到可执行文件！请先运行构建脚本构建应用程序。
    echo.
    echo 是否立即构建应用程序？(Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        cd packaging
        call build_exe.bat
    ) else (
        echo 已取消操作。
        
        rem 返回到packaging目录
        cd packaging
    )
) 