# 文件转换器

一个用于各种文件格式转换的工具，支持Word、Excel、Markdown、PDF、图片和文本文件的转换处理。

版权所有 (c) 2025 Junly

## 主要功能

- **Word转换功能**：将Word文档转换为Markdown、HTML，并支持保留图片
- **Word去除图片功能**：移除Word文档中的图片，并支持转换为多种格式
- **Excel转换功能**：将Excel文档转换为TXT、Markdown格式
- **Markdown表格转Excel功能**：提取Markdown中的表格数据转为Excel
- **Markdown转Word功能**：将Markdown文档转换为Word格式
- **PDF转换功能**：将PDF转换为Word、文本，以及提取图片
- **图片处理功能**：支持格式转换、尺寸调整和压缩
- **文本处理功能**：支持编码转换、格式转换和批量替换

## 系统要求

- Windows 7/10/11
- Python 3.8+
- 依赖库：PyQt6, python-docx, openpyxl, PyPDF2, Pillow等

## 安装

1. 克隆仓库或下载源代码
   ```
   git clone https://github.com/junly/file-converter.git
   ```

2. 安装依赖
   ```
   pip install -r requirements.txt
   ```

3. 运行程序
   ```
   python src/main.py
   ```

## 使用说明

### 单文件转换

1. 从主界面选择相应的功能标签页
2. 选择输入文件和输出位置
3. 配置转换选项
4. 点击"开始转换"按钮

### 批量处理

1. 从主界面选择要进行的转换类型
2. 点击"批量处理"按钮
3. 添加多个文件或整个文件夹
4. 选择输出目录
5. 点击"开始处理"按钮

## 目录结构

```
file-converter/
├── src/                # 源代码目录
│   ├── main.py         # 主程序入口
│   ├── ui/             # 用户界面模块
│   ├── core/           # 核心功能模块
│   ├── utils/          # 工具函数模块
│   └── resources/      # 资源文件
├── docs/               # 文档目录
├── requirements.txt    # 依赖项列表
└── README.md           # 项目说明文档
```

## 许可证

版权所有 (c) 2025 Junly，保留所有权利。
