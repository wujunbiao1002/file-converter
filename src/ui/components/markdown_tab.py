#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件工具 - Markdown标签页
版权所有 (c) 2025 Junly
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QComboBox, QGroupBox,
    QCheckBox, QRadioButton, QButtonGroup, QMessageBox,
    QProgressBar, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QColor
from core.markdown.markdown_converter import MarkdownConverter

class MarkdownConversionThread(QThread):
    """Markdown转换线程"""
    progress_updated = pyqtSignal(int)
    conversion_completed = pyqtSignal(bool, str, object)
    
    def __init__(self, converter, input_files, output_dir, conversion_type):
        super().__init__()
        self.converter = converter
        self.input_files = input_files if isinstance(input_files, list) else [input_files]
        self.output_dir = output_dir
        self.conversion_type = conversion_type
    
    def run(self):
        """执行转换操作"""
        try:
            results = []
            
            # 处理所有文件
            for i, input_file in enumerate(self.input_files):
                try:
                    # 生成输出文件路径
                    filename = os.path.basename(input_file)
                    name_without_ext = os.path.splitext(filename)[0]
                    
                    # 根据转换类型确定输出文件扩展名
                    if self.conversion_type == "word":
                        ext = ".docx"
                    elif self.conversion_type == "excel":
                        ext = ".xlsx"
                    else:
                        ext = ".docx"
                    
                    output_path = os.path.join(self.output_dir, f"{name_without_ext}{ext}")
                    
                    # 读取文档
                    md_content = self.converter.read_markdown(input_file)
                    
                    # 根据转换类型选择不同的转换方法
                    if self.conversion_type == "word":
                        result = self.converter.to_word(
                            md_content, output_path,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.conversion_type == "excel":
                        result = self.converter.extract_tables_to_excel(
                            md_content, output_path,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    else:
                        results.append((input_file, "", False, f"不支持的转换类型: {self.conversion_type}"))
                except Exception as e:
                    results.append((input_file, "", False, str(e)))
                
                # 更新进度
                self.progress_updated.emit(int((i+1) / len(self.input_files) * 100))
            
            self.conversion_completed.emit(True, "转换成功", results)
            
        except Exception as e:
            self.conversion_completed.emit(False, str(e), None)

class MarkdownTab(QWidget):
    """Markdown转换标签页"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.input_file = ""
        self.converter = MarkdownConverter()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        
        # 文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QVBoxLayout()
        
        # 文件列表
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list)
        
        # 文件按钮区域
        button_layout = QHBoxLayout()
        
        add_files_button = QPushButton("添加文件")
        add_files_button.clicked.connect(self.add_files)
        button_layout.addWidget(add_files_button)
        
        add_dir_button = QPushButton("添加目录")
        add_dir_button.clicked.connect(self.add_directory)
        button_layout.addWidget(add_dir_button)
        
        clear_button = QPushButton("清空列表")
        clear_button.clicked.connect(self.clear_files)
        button_layout.addWidget(clear_button)
        
        file_layout.addLayout(button_layout)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出位置:"))
        self.output_path = QLineEdit()
        self.output_path.setText(self.config.get("default_output_path"))
        self.output_path.setReadOnly(True)
        output_layout.addWidget(self.output_path)
        
        output_button = QPushButton("选择...")
        output_button.clicked.connect(self.select_output_location)
        output_layout.addWidget(output_button)
        file_layout.addLayout(output_layout)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # 转换选项区域
        options_group = QGroupBox("转换选项")
        options_layout = QVBoxLayout()
        
        # 转换类型选择
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("转换类型:"))
        self.conversion_type = QComboBox()
        self.conversion_type.addItems([
            "Markdown转Word",
            "Markdown表格提取为Excel"
        ])
        type_layout.addWidget(self.conversion_type)
        options_layout.addLayout(type_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 进度条
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("转换进度:"))
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)
        
        # 转换按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.convert_button = QPushButton("开始转换")
        self.convert_button.clicked.connect(self.start_conversion)
        button_layout.addWidget(self.convert_button)
        layout.addLayout(button_layout)
        
        # 添加一些拉伸空间
        layout.addStretch()
        
        self.setLayout(layout)
    
    def add_files(self):
        """添加Markdown文件到处理列表"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择Markdown文档", "", "Markdown文档 (*.md)"
        )
        
        if file_paths:
            for file_path in file_paths:
                # 检查文件是否已在列表中
                if not self.is_file_in_list(file_path):
                    self.file_list.addItem(file_path)
    
    def add_directory(self):
        """添加目录中的所有Markdown文件"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择Markdown文档目录"
        )
        
        if dir_path:
            # 支持的Markdown文档扩展名
            extensions = ['.md', '.markdown']
            
            # 遍历目录，添加匹配的文件
            for root, _, files in os.walk(dir_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        file_path = os.path.join(root, file)
                        # 检查文件是否已在列表中
                        if not self.is_file_in_list(file_path):
                            self.file_list.addItem(file_path)
    
    def is_file_in_list(self, file_path):
        """检查文件是否已经在列表中"""
        for i in range(self.file_list.count()):
            if self.file_list.item(i).text() == file_path:
                return True
        return False
    
    def clear_files(self):
        """清空文件列表"""
        self.file_list.clear()
    
    def browse_input_file(self):
        """浏览输入文件 (兼容旧方法)"""
        self.add_files()
    
    def set_input_file(self, file_path):
        """设置输入文件路径 (兼容旧方法)"""
        # 检查文件是否已在列表中
        if not self.is_file_in_list(file_path):
            self.file_list.addItem(file_path)
    
    def select_output_location(self):
        """选择输出位置"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择输出目录", self.output_path.text()
        )
        
        if dir_path:
            self.output_path.setText(dir_path)
    
    def start_conversion(self):
        """开始转换过程"""
        # 检查文件列表
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加输入文件")
            return
        
        # 获取所有文件路径
        input_files = []
        for i in range(self.file_list.count()):
            input_files.append(self.file_list.item(i).text())
        
        # 获取输出目录
        output_dir = self.output_path.text()
        if not output_dir:
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
        
        # 检查输出目录是否存在，如果不存在则创建
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建输出目录失败: {str(e)}")
                return
        
        # 获取转换选项
        conversion_index = self.conversion_type.currentIndex()
        
        # 根据选择的转换类型确定转换参数
        if conversion_index == 0:  # Markdown转Word
            conversion_type = "word"
        elif conversion_index == 1:  # Markdown表格提取为Excel
            conversion_type = "excel"
        
        # 启动转换线程
        self.progress_bar.setValue(0)
        self.convert_button.setEnabled(False)
        
        self.conversion_thread = MarkdownConversionThread(
            self.converter, input_files, output_dir, conversion_type
        )
        self.conversion_thread.progress_updated.connect(self.update_progress)
        self.conversion_thread.conversion_completed.connect(self.conversion_finished)
        self.conversion_thread.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def conversion_finished(self, success, message, results):
        """转换完成处理"""
        self.convert_button.setEnabled(True)
        
        if success and results:
            # 显示详细的转换结果
            success_count = sum(1 for _, _, status, _ in results if status)
            
            if success_count == len(results):
                QMessageBox.information(self, "转换完成", f"成功转换 {success_count} 个文件！")
            else:
                fail_count = len(results) - success_count
                detailed_msg = f"成功: {success_count} 个文件\n失败: {fail_count} 个文件\n\n"
                
                # 添加失败文件的详细信息
                for input_file, _, status, error in results:
                    if not status:
                        detailed_msg += f"文件 {os.path.basename(input_file)} 失败: {error}\n"
                
                QMessageBox.warning(self, "转换完成(部分失败)", detailed_msg)
        elif not success:
            QMessageBox.critical(self, "转换失败", f"错误: {message}") 