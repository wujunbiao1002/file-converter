@echo off
chcp 65001 >nul
echo 正在收集所有打包相关文件到packaging目录...

rem 确保packaging目录存在
if not exist packaging mkdir packaging

rem 复制打包相关文件
copy file_converter.spec packaging\file_converter.spec
copy build_exe.bat packaging\build_exe.bat
copy build_exe_small.bat packaging\build_exe_small.bat
copy install_upx.bat packaging\install_upx.bat
copy file_version_info.txt packaging\file_version_info.txt
copy README_OPTIMIZE.md packaging\README_OPTIMIZE.md
copy README_PACKAGE.md packaging\README_PACKAGE.md 2>nul

rem 创建run_app.bat的副本(从packaging目录运行)
echo @echo off > packaging\run_app.bat
echo chcp 65001 ^>nul >> packaging\run_app.bat
echo echo 正在启动Junly文件工具... >> packaging\run_app.bat
echo. >> packaging\run_app.bat
echo rem 设置工作目录为项目根目录 >> packaging\run_app.bat
echo cd .. >> packaging\run_app.bat
echo. >> packaging\run_app.bat
echo if exist "dist\Junly文件工具\Junly文件工具.exe" ( >> packaging\run_app.bat
echo     start "" "dist\Junly文件工具\Junly文件工具.exe" >> packaging\run_app.bat
echo ) else ( >> packaging\run_app.bat
echo     echo 未找到可执行文件！请先运行build_exe.bat构建应用程序。 >> packaging\run_app.bat
echo     echo. >> packaging\run_app.bat
echo     echo 是否立即构建应用程序？(Y/N) >> packaging\run_app.bat
echo     set /p choice= >> packaging\run_app.bat
echo     if /i "%%choice%%"=="Y" ( >> packaging\run_app.bat
echo         cd packaging >> packaging\run_app.bat
echo         call build_exe.bat >> packaging\run_app.bat
echo     ) else ( >> packaging\run_app.bat
echo         echo 已取消操作。 >> packaging\run_app.bat
echo     ) >> packaging\run_app.bat
echo ) >> packaging\run_app.bat
echo. >> packaging\run_app.bat
echo rem 返回到packaging目录 >> packaging\run_app.bat
echo cd packaging >> packaging\run_app.bat

rem 创建clean.bat的副本(从packaging目录运行)
echo @echo off > packaging\clean.bat
echo chcp 65001 ^>nul >> packaging\clean.bat
echo echo 开始清理项目临时文件和构建目录... >> packaging\clean.bat
echo. >> packaging\clean.bat
echo rem 设置工作目录为项目根目录 >> packaging\clean.bat
echo cd .. >> packaging\clean.bat
echo. >> packaging\clean.bat
echo rem 清理构建目录 >> packaging\clean.bat
echo if exist dist rmdir /s /q dist >> packaging\clean.bat
echo if exist build rmdir /s /q build >> packaging\clean.bat
echo if exist "*.spec" ( >> packaging\clean.bat
echo     for %%%%i in (*.spec) do ( >> packaging\clean.bat
echo         if not "%%%%i"=="file_converter.spec" del /f /q "%%%%i" >> packaging\clean.bat
echo     ) >> packaging\clean.bat
echo ) >> packaging\clean.bat
echo. >> packaging\clean.bat
echo rem 清理Python缓存文件 >> packaging\clean.bat
echo echo 清理Python缓存文件... >> packaging\clean.bat
echo FOR /d /r . %%%%d IN (__pycache__) DO @IF EXIST "%%%%d" rd /s /q "%%%%d" >> packaging\clean.bat
echo FOR /d /r . %%%%d IN (*.egg-info) DO @IF EXIST "%%%%d" rd /s /q "%%%%d" >> packaging\clean.bat
echo FOR /r . %%%%f IN (*.pyc) DO @IF EXIST "%%%%f" del /f /q "%%%%f" >> packaging\clean.bat
echo. >> packaging\clean.bat
echo rem 清理其他临时文件 >> packaging\clean.bat
echo echo 清理其他临时文件... >> packaging\clean.bat
echo del /f /q *.log 2^>nul >> packaging\clean.bat
echo del /f /q *.tmp 2^>nul >> packaging\clean.bat
echo del /f /q *.bak 2^>nul >> packaging\clean.bat
echo. >> packaging\clean.bat
echo echo 清理完成！ >> packaging\clean.bat
echo. >> packaging\clean.bat
echo rem 返回到packaging目录 >> packaging\clean.bat
echo cd packaging >> packaging\clean.bat
echo. >> packaging\clean.bat
echo pause >> packaging\clean.bat

echo 所有打包相关文件已收集到packaging目录中。
echo 现在您可以使用packaging目录下的脚本进行打包操作。
pause 