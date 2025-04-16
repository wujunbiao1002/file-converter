# Junly文件工具打包说明

本文档介绍如何将Junly文件工具项目打包成Windows可执行(exe)文件。

## 准备工作

1. 确保已安装Python 3.8或更高版本
2. 确保已安装项目依赖：`pip install -r requirements.txt`
3. 确保已安装PyInstaller：`pip install pyinstaller`

## 打包方法

### 方法一：使用批处理脚本（推荐）

直接运行项目根目录下的`build_exe.bat`批处理文件：

1. 双击`build_exe.bat`文件
2. 等待打包过程完成
3. 打包完成后，可执行文件将位于`dist/Junly文件工具`目录中
4. 构建完成后，脚本会自动清理临时文件和构建目录

### 方法二：手动执行PyInstaller命令

如果批处理脚本无法正常工作，可以手动执行以下步骤：

1. 打开命令提示符(CMD)或PowerShell
2. 切换到项目根目录
3. 执行以下命令：
   ```
   pyinstaller --clean file_converter.spec
   ```
4. 打包完成后，可执行文件将位于`dist/Junly文件工具`目录中
5. 可以通过运行`clean.bat`脚本清理临时文件

## 项目工具脚本

项目提供了以下批处理脚本，方便开发和使用：

- `build_exe.bat`: 构建可执行文件，并自动清理临时文件
- `clean.bat`: 清理项目中的临时文件和构建目录
- `run_app.bat`: 快速启动已构建的应用程序，如果应用未构建会提示构建

## 打包文件说明

- `file_converter.spec`：PyInstaller配置文件，定义打包参数和资源
- `file_version_info.txt`：定义EXE文件的版本信息
- `build_exe.bat`：自动化打包脚本

## 如何使用打包后的程序

1. 打开`dist/Junly文件工具`目录
2. 运行`Junly文件工具.exe`文件即可启动程序
3. 所有必要的依赖和资源文件都已打包在同一目录下

或者，可以直接双击项目根目录下的`run_app.bat`脚本快速启动程序。

## 常见问题

### 程序闪退

如果程序启动后立即关闭，可能是由于以下原因：

1. 缺少必要的运行时依赖
2. 程序初始化过程中出现错误

解决方法：
- 尝试从命令行启动程序以查看错误信息：
  ```
  cd dist\Junly文件工具
  Junly文件工具.exe
  ```

### 文件大小过大

PyInstaller打包会包含所有依赖，因此文件可能较大。如需进一步优化大小：

1. 修改`file_converter.spec`文件，在`excludes`列表中添加不需要的模块
2. 使用UPX压缩可执行文件（PyInstaller已集成此功能）

## 发布注意事项

发布程序时，需要分发整个`dist/Junly文件工具`目录，而不仅仅是exe文件。 