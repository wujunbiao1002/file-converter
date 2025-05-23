# 打包文件目录说明

本目录包含所有与应用程序打包相关的文件和脚本。这些文件被整理到一起，以便于管理和使用。

## 文件说明

| 文件名 | 用途 |
|--------|------|
| `file_converter.spec` | PyInstaller配置文件，定义打包参数和资源 |
| `build_exe.bat` | 标准打包脚本，构建可执行文件并自动清理临时文件 |
| `build_exe_small.bat` | 优化版打包脚本，生成体积更小的可执行文件 |
| `install_upx.bat` | 安装UPX压缩工具的脚本，用于减小可执行文件体积 |
| `file_version_info.txt` | 定义EXE文件的版本信息 |
| `clean.bat` | 清理项目中的临时文件和构建目录 |
| `run_app.bat` | 快速启动已构建的应用程序 |
| `README_OPTIMIZE.md` | 优化打包体积的指南 |
| `README_PACKAGE.md` | 详细的打包说明文档 |

## 使用方法

### 标准打包

1. 双击 `build_exe.bat` 文件
2. 等待打包过程完成
3. 打包完成后，可执行文件将位于项目根目录的 `dist/Junly文件转换工具` 目录中

### 优化体积打包

1. 如果需要安装UPX压缩工具，先运行 `install_upx.bat`
2. 双击 `build_exe_small.bat` 文件
3. 等待打包过程完成
4. 打包完成后，体积更小的可执行文件将位于项目根目录的 `dist/Junly文件转换工具` 目录中

### 清理临时文件

如果需要清理项目中的临时文件和构建目录，双击运行 `clean.bat`

### 启动应用程序

双击 `run_app.bat` 可以快速启动已构建的应用程序，如果应用未构建会提示构建

### 更多详细信息

- 关于打包的详细说明，请查看 `README_PACKAGE.md`
- 关于优化打包体积的指南，请查看 `README_OPTIMIZE.md`

## 注意事项

- 所有批处理脚本应在项目根目录运行，不要单独将这些文件复制到其他目录
- 发布程序时，需要分发整个 `dist/Junly文件转换工具` 目录，而不仅仅是exe文件 