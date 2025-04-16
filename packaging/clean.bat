@echo off
chcp 65001 >nul
echo 开始清理项目临时文件和构建目录...

rem 设置工作目录为项目根目录
cd ..

rem 清理构建目录
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist "*.spec" (
    for %%i in (*.spec) do (
        if not "%%i"=="file_converter.spec" del /f /q "%%i"
    )
)

rem 清理Python缓存文件
echo 清理Python缓存文件...
FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
FOR /d /r . %%d IN (*.egg-info) DO @IF EXIST "%%d" rd /s /q "%%d"
FOR /r . %%f IN (*.pyc) DO @IF EXIST "%%f" del /f /q "%%f"

rem 清理其他临时文件
echo 清理其他临时文件...
del /f /q *.log 2>nul
del /f /q *.tmp 2>nul
del /f /q *.bak 2>nul

rem 返回到packaging目录
cd packaging

echo.
echo 清理完成！
pause 