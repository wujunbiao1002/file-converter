#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 Markdown 表格转 Word 时的自适应宽度功能
"""

import os
import sys
import tempfile

# 将当前目录加入 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.markdown.markdown_converter import MarkdownConverter

def test_table_autofit():
    """
    测试将包含表格的 Markdown 转换为 Word 文档，表格列宽根据内容自适应
    """
    # 创建一个包含不同列文本长度的表格的 Markdown 文本
    md_content = """
# 测试表格自适应宽度

这是一个测试表格：

| 标题 | 年龄 | 详细描述 |
| --- | --- | --- |
| 张三 | 30 | 这是一个非常长的描述，用于测试列宽自适应功能是否生效 |
| 李四 | 25 | 中等长度的描述文本 |
| 王五 | 40 | 较短描述 |

表格结束。
"""

    # 创建临时文件路径
    temp_file = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
    temp_file.close()
    output_path = temp_file.name

    try:
        # 初始化转换器并执行转换
        converter = MarkdownConverter()
        result = converter.to_word(md_content, output_path)

        print(f"Markdown 转换完成，输出文件: {output_path}")
        print(f"请打开文件查看表格列宽是否根据内容自适应")
        print(f"预期结果: '详细描述'列应该比'年龄'列宽，'年龄'列应该是最窄的")
        
        return output_path
    except Exception as e:
        print(f"转换失败：{str(e)}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return None

if __name__ == "__main__":
    output_file = test_table_autofit()
    if output_file:
        # 在Windows下打开生成的文件
        if sys.platform.startswith('win'):
            os.system(f'start {output_file}')
        # 在macOS下打开生成的文件
        elif sys.platform.startswith('darwin'):
            os.system(f'open {output_file}')
        # 在Linux下打开生成的文件
        elif sys.platform.startswith('linux'):
            os.system(f'xdg-open {output_file}') 