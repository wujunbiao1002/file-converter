# -*- mode: python ; coding: utf-8 -*-
"""
Junly文件转换工具打包配置文件
"""

import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

# 获取项目根目录路径（相对于packaging目录的上一级）
base_path = os.path.abspath(os.path.join(os.path.dirname(SPEC), '..'))

block_cipher = None

# 收集必要的依赖，使用更完整的导入以确保应用正常运行
hiddenimports = []
# 基础PyQt6组件
hiddenimports += collect_submodules('PyQt6')
# 文档处理模块
hiddenimports += collect_submodules('docx')
hiddenimports += collect_submodules('openpyxl')
hiddenimports += collect_submodules('PyPDF2')
hiddenimports += collect_submodules('PIL')
hiddenimports += collect_submodules('markdown')
# 数据处理模块
hiddenimports += collect_submodules('pandas')
# 必要的系统模块
hiddenimports += ['email', 'email.parser', 'email.mime', 'email.utils']
hiddenimports += ['calendar', 'datetime', 'time', 'json']
hiddenimports += ['collections', 'itertools', 'functools']
# XML处理
hiddenimports += collect_submodules('lxml')
hiddenimports += ['bs4', 'beautifulsoup4']
# 确保系统特定模块包含
if sys.platform.startswith('win'):
    hiddenimports += ['win32com', 'win32api', 'win32con']
    hiddenimports += ['comtypes']

# 收集资源文件
datas = []
datas += [(os.path.join(base_path, 'src/assets/'), 'assets/')]
datas += [(os.path.join(base_path, 'src/ui/themes/'), 'ui/themes/')]

# 排除不必要的模块和包 - 减少排除项以确保应用正常运行
excludes = [
    'tkinter', 'matplotlib', 'scipy', 'sympy', 'ipython', 
    'sklearn', 'nose', 'mock', 'sphinx', 
    'pytest', 'unittest', 'setuptools',
    'PyQt5', 'PySide6'
]

# 创建可执行文件配置
a = Analysis(
    [os.path.join(base_path, 'src/main.py')],
    pathex=[base_path],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 仅过滤明确不需要的文件
def filter_binaries(binaries):
    return [b for b in binaries if not (
        b[0].endswith('.pyc') or 
        '__pycache__' in b[0] or 
        b[0].endswith('.pyo') or
        'tests/test_' in b[0].lower() or
        'unittest' in b[0].lower() or
        'pytest' in b[0].lower()
    )]

# 仅过滤明确不需要的数据文件
def filter_datas(datas):
    return [d for d in datas if not (
        '__pycache__' in d[0].lower() or
        'tests/test_' in d[0].lower() or
        'unittest' in d[0].lower() or
        'pytest' in d[0].lower()
    )]

a.binaries = filter_binaries(a.binaries)
a.datas = filter_datas(a.datas)

# 构建PYZ
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

# 构建EXE
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Junly文件转换工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # 不去除符号表以确保稳定性
    upx=True,     # 使用UPX压缩
    upx_exclude=['vcruntime140.dll', 'python*.dll', 'VCRUNTIME140.dll', 'MSVCP140.dll', 'api-ms-*.dll'],
    console=False, # 关闭控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(base_path, 'src/assets/logo.png'),
    version=os.path.join(os.path.dirname(SPEC), 'file_version_info.txt'),
)

# 收集所有文件
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,  # 不去除符号表以确保稳定性
    upx=True,     # 使用UPX压缩
    upx_exclude=['vcruntime140.dll', 'python*.dll', 'VCRUNTIME140.dll', 'MSVCP140.dll', 'api-ms-*.dll'],
    name='Junly文件转换工具',
) 