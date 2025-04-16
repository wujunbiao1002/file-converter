#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件工具 - 文本处理模块
版权所有 (c) 2025 Junly
"""

import os
import codecs
import re
from bs4 import BeautifulSoup

class TextProcessor:
    """文本处理类，提供编码转换、格式转换和批量替换功能"""
    
    def __init__(self):
        """初始化文本处理器"""
        self.replace_rules = []
    
    def set_replace_rules(self, rules_text):
        """设置替换规则
        
        Args:
            rules_text (str): 替换规则文本，每行一条规则，格式: 原文本->替换文本
        """
        self.replace_rules = []
        lines = rules_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or '->' not in line:
                continue
                
            parts = line.split('->', 1)
            if len(parts) == 2:
                source, target = parts[0].strip(), parts[1].strip()
                if source:
                    self.replace_rules.append((source, target))
    
    def convert_encoding(self, input_file, output_file, target_encoding, progress_callback=None):
        """转换文件编码
        
        Args:
            input_file (str): 输入文件路径
            output_file (str): 输出文件路径
            target_encoding (str): 目标编码
            progress_callback (function): 进度回调函数
            
        Returns:
            bool: 是否成功
        """
        try:
            # 尝试检测源文件编码
            encodings_to_try = ['utf-8', 'gbk', 'utf-16', 'ascii', 'latin-1']
            content = None
            
            for encoding in encodings_to_try:
                try:
                    with codecs.open(input_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise Exception("无法检测输入文件的编码")
            
            if progress_callback:
                progress_callback(50)
                
            # 以目标编码写入文件
            with codecs.open(output_file, 'w', encoding=target_encoding) as f:
                f.write(content)
                
            if progress_callback:
                progress_callback(100)
                
            return True
            
        except Exception as e:
            raise Exception(f"编码转换失败: {str(e)}")
    
    def text_to_html(self, input_file, output_file, progress_callback=None):
        """将文本文件转换为HTML
        
        Args:
            input_file (str): 输入文件路径
            output_file (str): 输出文件路径
            progress_callback (function): 进度回调函数
            
        Returns:
            bool: 是否成功
        """
        try:
            # 读取文本文件内容
            encodings_to_try = ['utf-8', 'gbk', 'utf-16', 'ascii', 'latin-1']
            content = None
            
            for encoding in encodings_to_try:
                try:
                    with codecs.open(input_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise Exception("无法检测输入文件的编码")
                
            if progress_callback:
                progress_callback(30)
            
            # 转换为HTML
            html_content = "<!DOCTYPE html>\n<html>\n<head>\n"
            html_content += "<meta charset=\"UTF-8\">\n"
            html_content += "<title>转换自文本文件</title>\n"
            html_content += "<style>\n"
            html_content += "body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }\n"
            html_content += "pre { background-color: #f5f5f5; padding: 10px; border-radius: 5px; white-space: pre-wrap; }\n"
            html_content += "</style>\n"
            html_content += "</head>\n<body>\n"
            
            # 处理内容
            html_content += "<pre>" + self._escape_html(content) + "</pre>\n"
            
            html_content += "</body>\n</html>"
            
            if progress_callback:
                progress_callback(70)
                
            # 写入HTML文件
            with codecs.open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            if progress_callback:
                progress_callback(100)
                
            return True
            
        except Exception as e:
            raise Exception(f"转换HTML失败: {str(e)}")
    
    def text_to_markdown(self, input_file, output_file, progress_callback=None):
        """将文本文件转换为Markdown
        
        Args:
            input_file (str): 输入文件路径
            output_file (str): 输出文件路径
            progress_callback (function): 进度回调函数
            
        Returns:
            bool: 是否成功
        """
        try:
            # 读取文本文件内容
            encodings_to_try = ['utf-8', 'gbk', 'utf-16', 'ascii', 'latin-1']
            content = None
            
            for encoding in encodings_to_try:
                try:
                    with codecs.open(input_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise Exception("无法检测输入文件的编码")
                
            if progress_callback:
                progress_callback(30)
            
            # 转换为Markdown (简单添加代码块)
            md_content = "# 转换自文本文件\n\n"
            md_content += "```\n" + content + "\n```\n"
            
            if progress_callback:
                progress_callback(70)
                
            # 写入Markdown文件
            with codecs.open(output_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            if progress_callback:
                progress_callback(100)
                
            return True
            
        except Exception as e:
            raise Exception(f"转换Markdown失败: {str(e)}")
    
    def batch_replace(self, input_file, output_file, progress_callback=None):
        """批量替换文本内容
        
        Args:
            input_file (str): 输入文件路径
            output_file (str): 输出文件路径
            progress_callback (function): 进度回调函数
            
        Returns:
            bool: 是否成功
        """
        try:
            if not self.replace_rules:
                raise Exception("未设置替换规则")
                
            # 读取文本文件内容
            encodings_to_try = ['utf-8', 'gbk', 'utf-16', 'ascii', 'latin-1']
            content = None
            
            for encoding in encodings_to_try:
                try:
                    with codecs.open(input_file, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                raise Exception("无法检测输入文件的编码")
                
            if progress_callback:
                progress_callback(30)
            
            # 执行替换
            for source, target in self.replace_rules:
                content = content.replace(source, target)
                
            if progress_callback:
                progress_callback(70)
                
            # 写入输出文件
            with codecs.open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            if progress_callback:
                progress_callback(100)
                
            return True
            
        except Exception as e:
            raise Exception(f"批量替换失败: {str(e)}")
    
    def _escape_html(self, text):
        """HTML转义
        
        Args:
            text (str): 原文本
            
        Returns:
            str: 转义后的文本
        """
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#39;") 