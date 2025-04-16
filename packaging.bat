@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

title Junly文件工具 - 打包管理

:menu
cls
echo ======================================
echo      Junly文件工具 - 打包管理菜单
echo ======================================
echo.
echo  [1] 标准构建应用程序
echo  [2] 优化构建应用程序 (更小)
echo  [3] 安装UPX压缩工具
echo  [4] 清理临时文件
echo  [5] 启动应用程序
echo  [6] 打开packaging目录
echo  [7] 查看打包说明文档
echo  [0] 退出
echo.
echo ======================================
echo.

set /p choice=请选择操作 [0-7]: 

if "%choice%"=="1" (
    cd packaging
    call build_exe.bat
    cd ..
    goto menu
)

if "%choice%"=="2" (
    cd packaging
    call build_exe_small.bat
    cd ..
    goto menu
)

if "%choice%"=="3" (
    cd packaging
    call install_upx.bat
    cd ..
    goto menu
)

if "%choice%"=="4" (
    cd packaging
    call clean.bat
    cd ..
    goto menu
)

if "%choice%"=="5" (
    cd packaging
    call run_app.bat
    cd ..
    goto menu
)

if "%choice%"=="6" (
    start "" "packaging"
    goto menu
)

if "%choice%"=="7" (
    start "" "packaging\README.md"
    goto menu
)

if "%choice%"=="0" (
    exit /b
) else (
    echo.
    echo 无效的选择，请重试...
    timeout /t 2 >nul
    goto menu
)

endlocal 