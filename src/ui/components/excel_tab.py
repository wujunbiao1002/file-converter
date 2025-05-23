#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件转换工具 - Excel标签页
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
from core.excel.excel_converter import ExcelConverter

class ExcelConversionThread(QThread):
    """Excel转换线程"""
    progress_updated = pyqtSignal(int)
    conversion_completed = pyqtSignal(bool, str, object)
    
    def __init__(self, converter, input_files, output_dir, conversion_type):
        super().__init__()
        self.converter = converter
        self.input_files = input_files if isinstance(input_files, list) else [input_files]
        self.output_dir = output_dir
        self.conversion_type = conversion_type
        self.running = True
    
    def run(self):
        """执行转换操作"""
        try:
            results = []
            
            # 处理所有文件
            for i, input_file in enumerate(self.input_files):
                if not self.running:
                    break
                    
                try:
                    # 生成输出文件路径
                    filename = os.path.basename(input_file)
                    name_without_ext = os.path.splitext(filename)[0]
                    
                    # 根据转换类型确定输出文件扩展名
                    if self.conversion_type == "txt":
                        ext = ".txt"
                    elif self.conversion_type == "markdown":
                        ext = ".md"
                    else:
                        ext = ".txt"
                    
                    output_path = os.path.join(self.output_dir, f"{name_without_ext}{ext}")
                    
                    # 读取文档
                    workbook = self.converter.read_excel(input_file)
                    
                    # 根据转换类型选择不同的转换方法
                    if self.conversion_type == "txt":
                        result = self.converter.save_as_txt(
                            workbook, output_path,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.conversion_type == "markdown":
                        # 执行转换
                        result = self.converter.save_as_markdown(
                            workbook, output_path,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        
                        # 检查是否有多个工作表
                        if len(workbook.sheetnames) > 1:
                            # 如有多工作表，记录所有可能的输出文件路径
                            multiple_outputs = []
                            base_name, _ = os.path.splitext(output_path)
                            for sheet_name in workbook.sheetnames:
                                sheet_output_path = f"{base_name}-{sheet_name}.md"
                                multiple_outputs.append(sheet_output_path)
                            
                            # 在结果中标记它有多个输出文件
                            results.append((input_file, multiple_outputs, True, "多Sheet文档，已为每个Sheet生成单独的MD文件"))
                        else:
                            # 单工作表情况
                            results.append((input_file, output_path, True, ""))
                    else:
                        results.append((input_file, "", False, f"不支持的转换类型: {self.conversion_type}"))
                except Exception as e:
                    results.append((input_file, "", False, str(e)))
                
                # 更新进度
                self.progress_updated.emit(int((i+1) / len(self.input_files) * 100))
            
            if self.running:
                self.conversion_completed.emit(True, "转换成功", results)
            
        except Exception as e:
            if self.running:
                self.conversion_completed.emit(False, str(e), None)
    
    def stop(self):
        """停止转换操作"""
        self.running = False

class ExcelTab(QWidget):
    """Excel转换标签页"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.input_file = ""
        self.converter = ExcelConverter()
        self.conversion_thread = None
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
            "Excel转TXT",
            "Excel转Markdown"
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
        """添加Excel文件到处理列表"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择Excel文档", "", "Excel文档 (*.xlsx *.xls)"
        )
        
        if file_paths:
            for file_path in file_paths:
                # 检查文件是否已在列表中
                if not self.is_file_in_list(file_path):
                    self.file_list.addItem(file_path)
    
    def add_directory(self):
        """添加目录中的所有Excel文件"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择Excel文档目录"
        )
        
        if dir_path:
            # 支持的Excel文档扩展名
            extensions = ['.xlsx', '.xls']
            
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
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取转换类型
        index = self.conversion_type.currentIndex()
        if index == 0:
            conversion_type = "txt"
        elif index == 1:
            conversion_type = "markdown"
        else:
            conversion_type = "txt"
        
        # 禁用转换按钮
        self.convert_button.setEnabled(False)
        self.convert_button.setText("正在转换...")
        
        # 重置进度条
        self.progress_bar.setValue(0)
        
        # 开始转换线程
        # 如果存在旧线程，先停止并等待完成
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.stop()
            self.conversion_thread.wait()
            
        # 创建并启动新的转换线程
        self.conversion_thread = ExcelConversionThread(
            self.converter, input_files, output_dir, conversion_type
        )
        self.conversion_thread.progress_updated.connect(self.update_progress)
        self.conversion_thread.conversion_completed.connect(self.conversion_finished)
        self.conversion_thread.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def conversion_finished(self, success, message, results):
        """转换完成后的处理"""
        # 重新启用转换按钮
        self.convert_button.setEnabled(True)
        self.convert_button.setText("开始转换")
        
        if success:
            # 检查是否有多工作表转换情况
            has_multi_sheet = False
            result_message = "Excel文档转换成功!"
            
            if results:
                for _, output_path, _, info in results:
                    if isinstance(output_path, list) or (info and "多Sheet文档" in info):
                        has_multi_sheet = True
                        break
            
            if has_multi_sheet:
                result_message = "Excel文档转换成功!\n\n注意：检测到多工作表Excel文件，已为每个工作表创建单独的Markdown文件。"
            
            QMessageBox.information(self, "转换成功", result_message)
        else:
            QMessageBox.critical(self, "转换失败", f"转换过程中发生错误:\n{message}")
    
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 确保线程在窗口关闭时停止
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.stop()
            self.conversion_thread.wait()
        super().closeEvent(event) 