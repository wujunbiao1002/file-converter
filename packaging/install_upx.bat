@echo off
chcp 65001 >nul
echo 正在下载并安装UPX压缩工具...

rem 设置工作目录为项目根目录
cd ..

rem 创建临时目录
if not exist temp mkdir temp
cd temp

rem 下载UPX
echo 正在下载UPX...
curl -L -o upx.zip https://github.com/upx/upx/releases/download/v4.2.2/upx-4.2.2-win64.zip

rem 解压缩UPX
echo 正在解压UPX...
powershell -command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Expand-Archive -Force upx.zip .}"

rem 将UPX添加到PyInstaller的搜索路径
echo 正在将UPX放入适当的位置...
set PYINSTALLER_PATH=..\\.venv\\Lib\\site-packages\\PyInstaller
if not exist "%PYINSTALLER_PATH%\\utils\\upx" mkdir "%PYINSTALLER_PATH%\\utils\\upx"
copy upx-4.2.2-win64\\upx.exe "%PYINSTALLER_PATH%\\utils\\upx\\upx.exe"

rem 清理临时文件
cd ..
echo 正在清理临时文件...
rmdir /s /q temp

rem 返回到packaging目录
cd packaging

echo UPX安装完成！
echo.
echo 你现在可以使用build_exe_small.bat脚本编译更小的可执行文件。
pause 