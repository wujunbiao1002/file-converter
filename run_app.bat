@echo off
chcp 65001 >nul
echo 正在启动Junly文件工具...

if exist "dist\Junly文件工具\Junly文件工具.exe" (
    start "" "dist\Junly文件工具\Junly文件工具.exe"
) else (
    echo 未找到可执行文件！请先运行build_exe.bat构建应用程序。
    echo.
    echo 是否立即构建应用程序？(Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        call build_exe.bat
    ) else (
        echo 已取消操作。
    )
) 