#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 文本处理标签页
版权所有 (c) 2025 Junly
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QComboBox, QGroupBox,
    QCheckBox, QRadioButton, QButtonGroup, QMessageBox,
    QProgressBar, QTextEdit, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QColor
from core.text.text_processor import TextProcessor

class TextProcessingThread(QThread):
    """文本处理线程"""
    progress_updated = pyqtSignal(int)
    processing_completed = pyqtSignal(bool, str, object)
    
    def __init__(self, processor, input_files, output_dir, operation_type, encoding=None):
        super().__init__()
        self.processor = processor
        self.input_files = input_files if isinstance(input_files, list) else [input_files]
        self.output_dir = output_dir
        self.operation_type = operation_type
        self.encoding = encoding
    
    def run(self):
        """执行处理操作"""
        try:
            results = []
            
            # 处理所有文件
            for i, input_file in enumerate(self.input_files):
                try:
                    # 生成输出文件路径
                    filename = os.path.basename(input_file)
                    name_without_ext = os.path.splitext(filename)[0]
                    
                    # 根据处理类型确定输出文件扩展名
                    if self.operation_type == "encoding_convert":
                        ext = ".txt"
                    elif self.operation_type == "to_html":
                        ext = ".html"
                    elif self.operation_type == "to_markdown":
                        ext = ".md"
                    elif self.operation_type == "batch_replace":
                        ext = ".txt"
                    else:
                        ext = ".txt"
                    
                    output_path = os.path.join(self.output_dir, f"{name_without_ext}{ext}")
                    
                    # 根据处理类型选择不同的方法
                    if self.operation_type == "encoding_convert":
                        result = self.processor.convert_encoding(
                            input_file, output_path, self.encoding,
                            lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.operation_type == "to_html":
                        result = self.processor.text_to_html(
                            input_file, output_path,
                            lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.operation_type == "to_markdown":
                        result = self.processor.text_to_markdown(
                            input_file, output_path,
                            lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.operation_type == "batch_replace":
                        result = self.processor.batch_replace(
                            input_file, output_path,
                            lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    else:
                        results.append((input_file, "", False, f"不支持的处理类型: {self.operation_type}"))
                except Exception as e:
                    results.append((input_file, "", False, str(e)))
                
                # 更新进度
                self.progress_updated.emit(int((i+1) / len(self.input_files) * 100))
            
            self.processing_completed.emit(True, "处理成功", results)
            
        except Exception as e:
            self.processing_completed.emit(False, str(e), None)

class TextTab(QWidget):
    """文本处理标签页"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.input_file = ""
        self.processor = TextProcessor()
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
        
        # 处理选项区域
        options_group = QGroupBox("处理选项")
        options_layout = QVBoxLayout()
        
        # 处理类型选择
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("处理类型:"))
        self.operation_type = QComboBox()
        self.operation_type.addItems([
            "编码转换", 
            "文本转HTML", 
            "文本转Markdown",
            "批量替换"
        ])
        self.operation_type.currentIndexChanged.connect(self.update_options)
        type_layout.addWidget(self.operation_type)
        options_layout.addLayout(type_layout)
        
        # 编码选项
        encoding_layout = QHBoxLayout()
        encoding_layout.addWidget(QLabel("目标编码:"))
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems([
            "UTF-8", 
            "GBK", 
            "UTF-16",
            "ASCII",
            "Latin-1"
        ])
        encoding_layout.addWidget(self.encoding_combo)
        options_layout.addLayout(encoding_layout)
        
        # 批量替换设置
        self.replace_group = QGroupBox("替换设置")
        self.replace_group.setVisible(False)
        replace_layout = QVBoxLayout()
        
        replace_layout.addWidget(QLabel("替换规则 (每行一条，格式: 原文本->替换文本)"))
        self.replace_rules = QTextEdit()
        replace_layout.addWidget(self.replace_rules)
        
        self.replace_group.setLayout(replace_layout)
        options_layout.addWidget(self.replace_group)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 进度条
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("处理进度:"))
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        layout.addLayout(progress_layout)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.process_button = QPushButton("开始处理")
        self.process_button.clicked.connect(self.start_processing)
        button_layout.addWidget(self.process_button)
        layout.addLayout(button_layout)
        
        # 添加一些拉伸空间
        layout.addStretch()
        
        self.setLayout(layout)
        
        # 初始化显示/隐藏选项
        self.update_options()
    
    def update_options(self):
        """根据处理类型更新选项"""
        operation_index = self.operation_type.currentIndex()
        
        # 显示/隐藏编码选项
        self.encoding_combo.setVisible(operation_index == 0)  # 仅在编码转换时显示
        
        # 显示/隐藏批量替换设置
        self.replace_group.setVisible(operation_index == 3)  # 仅在批量替换时显示
    
    def add_files(self):
        """添加文本文件到处理列表"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择文本文件", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_paths:
            for file_path in file_paths:
                # 检查文件是否已在列表中
                if not self.is_file_in_list(file_path):
                    self.file_list.addItem(file_path)
    
    def add_directory(self):
        """添加目录中的所有文本文件"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择文本文件目录"
        )
        
        if dir_path:
            # 支持的文本文件扩展名
            extensions = ['.txt', '.text', '.log']
            
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
    
    def start_processing(self):
        """开始处理过程"""
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
        
        # 获取处理选项
        operation_index = self.operation_type.currentIndex()
        
        # 根据选择的处理类型确定处理参数
        if operation_index == 0:  # 编码转换
            operation_type = "encoding_convert"
            encoding = self.encoding_combo.currentText()
        elif operation_index == 1:  # 文本转HTML
            operation_type = "to_html"
            encoding = None
        elif operation_index == 2:  # 文本转Markdown
            operation_type = "to_markdown"
            encoding = None
        elif operation_index == 3:  # 批量替换
            operation_type = "batch_replace"
            encoding = None
            
            # 设置替换规则
            rules_text = self.replace_rules.toPlainText()
            if not rules_text.strip():
                QMessageBox.warning(self, "警告", "请输入替换规则")
                return
            
            # 解析并设置替换规则
            rules = []
            for line in rules_text.split("\n"):
                if "->" in line:
                    old, new = line.split("->", 1)
                    rules.append((old.strip(), new.strip()))
            
            if not rules:
                QMessageBox.warning(self, "警告", "没有有效的替换规则")
                return
            
            self.processor.set_replace_rules(rules)
            
        # 启动处理线程
        self.progress_bar.setValue(0)
        self.process_button.setEnabled(False)
        
        self.processing_thread = TextProcessingThread(
            self.processor, input_files, output_dir, operation_type, encoding
        )
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.processing_completed.connect(self.processing_finished)
        self.processing_thread.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def processing_finished(self, success, message, results):
        """处理完成处理"""
        self.process_button.setEnabled(True)
        
        if success and results:
            # 显示详细的处理结果
            success_count = sum(1 for _, _, status, _ in results if status)
            
            if success_count == len(results):
                QMessageBox.information(self, "处理完成", f"成功处理 {success_count} 个文件！")
            else:
                fail_count = len(results) - success_count
                detailed_msg = f"成功: {success_count} 个文件\n失败: {fail_count} 个文件\n\n"
                
                # 添加失败文件的详细信息
                for input_file, _, status, error in results:
                    if not status:
                        detailed_msg += f"文件 {os.path.basename(input_file)} 失败: {error}\n"
                
                QMessageBox.warning(self, "处理完成(部分失败)", detailed_msg)
        elif not success:
            QMessageBox.critical(self, "处理失败", f"错误: {message}") 