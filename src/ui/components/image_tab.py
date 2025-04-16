#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 图片标签页
版权所有 (c) 2025 Junly
"""

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QComboBox, QGroupBox,
    QCheckBox, QRadioButton, QButtonGroup, QMessageBox,
    QProgressBar, QTabWidget, QListWidget, QListWidgetItem,
    QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QColor
from core.image.image_processor import ImageProcessor

class ImageProcessingThread(QThread):
    """图片处理线程"""
    progress_updated = pyqtSignal(int)
    processing_completed = pyqtSignal(bool, str, object)
    
    def __init__(self, processor, operation_type, input_files, output_dir, params=None):
        super().__init__()
        self.processor = processor
        self.operation_type = operation_type
        self.input_files = input_files
        self.output_dir = output_dir
        self.params = params or {}
    
    def run(self):
        """执行图片处理操作"""
        try:
            # 根据操作类型执行不同的处理
            results = None
            if self.operation_type == "format_convert":
                target_format = self.params.get('target_format', 'jpg')
                results = self.processor.batch_convert_format(
                    self.input_files, self.output_dir, target_format,
                    progress_callback=lambda value: self.progress_updated.emit(value)
                )
            elif self.operation_type == "resize":
                width = self.params.get('width', 0)
                height = self.params.get('height', 0)
                keep_aspect_ratio = self.params.get('keep_aspect_ratio', True)
                results = self.processor.batch_resize_image(
                    self.input_files, self.output_dir, width, height, keep_aspect_ratio,
                    progress_callback=lambda value: self.progress_updated.emit(value)
                )
            elif self.operation_type == "compress":
                quality = self.params.get('quality', 85)
                results = self.processor.batch_compress_image(
                    self.input_files, self.output_dir, quality,
                    progress_callback=lambda value: self.progress_updated.emit(value)
                )
            else:
                raise Exception(f"不支持的操作类型: {self.operation_type}")
            
            self.processing_completed.emit(True, "处理完成", results)
            
        except Exception as e:
            self.processing_completed.emit(False, str(e), None)

class ImageTab(QWidget):
    """图片处理标签页"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.input_files = []
        self.processor = ImageProcessor()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()
        
        # 创建子标签页
        self.tabs = QTabWidget()
        
        # 创建各功能标签页
        self.format_tab = self.create_format_tab()
        self.resize_tab = self.create_resize_tab()
        self.compress_tab = self.create_compress_tab()
        
        # 添加子标签页
        self.tabs.addTab(self.format_tab, "格式转换")
        self.tabs.addTab(self.resize_tab, "尺寸调整")
        self.tabs.addTab(self.compress_tab, "图片压缩")
        
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def create_format_tab(self):
        """创建格式转换标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 文件选择区域
        file_group = QGroupBox("图片选择")
        file_layout = QVBoxLayout()
        
        # 文件列表
        self.format_file_list = QListWidget()
        file_layout.addWidget(self.format_file_list)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        add_files_button = QPushButton("添加图片")
        add_files_button.clicked.connect(lambda: self.add_files(self.format_file_list))
        button_layout.addWidget(add_files_button)
        
        add_dir_button = QPushButton("添加目录")
        add_dir_button.clicked.connect(lambda: self.add_directory(self.format_file_list))
        button_layout.addWidget(add_dir_button)
        
        clear_button = QPushButton("清空列表")
        clear_button.clicked.connect(lambda: self.clear_files(self.format_file_list))
        button_layout.addWidget(clear_button)
        
        file_layout.addLayout(button_layout)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # 转换选项区域
        options_group = QGroupBox("转换选项")
        options_layout = QVBoxLayout()
        
        # 目标格式选择
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("目标格式:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPG", "PNG", "BMP", "TIFF", "WEBP", "GIF"])
        format_layout.addWidget(self.format_combo)
        options_layout.addLayout(format_layout)
        
        # 输出目录选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.format_output_path = QLineEdit()
        self.format_output_path.setText(self.config.get("default_output_path"))
        self.format_output_path.setReadOnly(True)
        output_layout.addWidget(self.format_output_path)
        
        output_button = QPushButton("浏览...")
        output_button.clicked.connect(lambda: self.select_output_dir(self.format_output_path))
        output_layout.addWidget(output_button)
        options_layout.addLayout(output_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 进度条
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("处理进度:"))
        self.format_progress = QProgressBar()
        progress_layout.addWidget(self.format_progress)
        layout.addLayout(progress_layout)
        
        # 开始转换按钮
        start_layout = QHBoxLayout()
        start_layout.addStretch()
        self.format_start_button = QPushButton("开始转换")
        self.format_start_button.clicked.connect(lambda: self.start_processing("format_convert"))
        start_layout.addWidget(self.format_start_button)
        layout.addLayout(start_layout)
        
        tab.setLayout(layout)
        return tab
    
    def create_resize_tab(self):
        """创建尺寸调整标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 文件选择区域
        file_group = QGroupBox("图片选择")
        file_layout = QVBoxLayout()
        
        # 文件列表
        self.resize_file_list = QListWidget()
        file_layout.addWidget(self.resize_file_list)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        add_files_button = QPushButton("添加图片")
        add_files_button.clicked.connect(lambda: self.add_files(self.resize_file_list))
        button_layout.addWidget(add_files_button)
        
        add_dir_button = QPushButton("添加目录")
        add_dir_button.clicked.connect(lambda: self.add_directory(self.resize_file_list))
        button_layout.addWidget(add_dir_button)
        
        clear_button = QPushButton("清空列表")
        clear_button.clicked.connect(lambda: self.clear_files(self.resize_file_list))
        button_layout.addWidget(clear_button)
        
        file_layout.addLayout(button_layout)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # 调整选项区域
        options_group = QGroupBox("调整选项")
        options_layout = QVBoxLayout()
        
        # 尺寸设置
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("宽度:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 10000)
        self.width_spin.setValue(800)
        size_layout.addWidget(self.width_spin)
        
        size_layout.addWidget(QLabel("高度:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(0, 10000)
        self.height_spin.setValue(600)
        size_layout.addWidget(self.height_spin)
        options_layout.addLayout(size_layout)
        
        # 保持宽高比选项
        self.keep_aspect_ratio = QCheckBox("保持宽高比")
        self.keep_aspect_ratio.setChecked(True)
        options_layout.addWidget(self.keep_aspect_ratio)
        
        # 输出目录选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.resize_output_path = QLineEdit()
        self.resize_output_path.setText(self.config.get("default_output_path"))
        self.resize_output_path.setReadOnly(True)
        output_layout.addWidget(self.resize_output_path)
        
        output_button = QPushButton("浏览...")
        output_button.clicked.connect(lambda: self.select_output_dir(self.resize_output_path))
        output_layout.addWidget(output_button)
        options_layout.addLayout(output_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 进度条
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("处理进度:"))
        self.resize_progress = QProgressBar()
        progress_layout.addWidget(self.resize_progress)
        layout.addLayout(progress_layout)
        
        # 开始转换按钮
        start_layout = QHBoxLayout()
        start_layout.addStretch()
        self.resize_start_button = QPushButton("开始调整尺寸")
        self.resize_start_button.clicked.connect(lambda: self.start_processing("resize"))
        start_layout.addWidget(self.resize_start_button)
        layout.addLayout(start_layout)
        
        tab.setLayout(layout)
        return tab
    
    def create_compress_tab(self):
        """创建图片压缩标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 文件选择区域
        file_group = QGroupBox("图片选择")
        file_layout = QVBoxLayout()
        
        # 文件列表
        self.compress_file_list = QListWidget()
        file_layout.addWidget(self.compress_file_list)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        add_files_button = QPushButton("添加图片")
        add_files_button.clicked.connect(lambda: self.add_files(self.compress_file_list))
        button_layout.addWidget(add_files_button)
        
        add_dir_button = QPushButton("添加目录")
        add_dir_button.clicked.connect(lambda: self.add_directory(self.compress_file_list))
        button_layout.addWidget(add_dir_button)
        
        clear_button = QPushButton("清空列表")
        clear_button.clicked.connect(lambda: self.clear_files(self.compress_file_list))
        button_layout.addWidget(clear_button)
        
        file_layout.addLayout(button_layout)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # 压缩选项区域
        options_group = QGroupBox("压缩选项")
        options_layout = QVBoxLayout()
        
        # 质量设置
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("压缩质量:"))
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(85)
        quality_layout.addWidget(self.quality_spin)
        quality_layout.addWidget(QLabel("(1-100，值越低压缩率越高，但质量越低)"))
        options_layout.addLayout(quality_layout)
        
        # 输出目录选择
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.compress_output_path = QLineEdit()
        self.compress_output_path.setText(self.config.get("default_output_path"))
        self.compress_output_path.setReadOnly(True)
        output_layout.addWidget(self.compress_output_path)
        
        output_button = QPushButton("浏览...")
        output_button.clicked.connect(lambda: self.select_output_dir(self.compress_output_path))
        output_layout.addWidget(output_button)
        options_layout.addLayout(output_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # 进度条
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("处理进度:"))
        self.compress_progress = QProgressBar()
        progress_layout.addWidget(self.compress_progress)
        layout.addLayout(progress_layout)
        
        # 开始转换按钮
        start_layout = QHBoxLayout()
        start_layout.addStretch()
        self.compress_start_button = QPushButton("开始压缩")
        self.compress_start_button.clicked.connect(lambda: self.start_processing("compress"))
        start_layout.addWidget(self.compress_start_button)
        layout.addLayout(start_layout)
        
        tab.setLayout(layout)
        return tab
    
    def add_files(self, list_widget):
        """添加图片到处理列表"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择图片", "", 
            "图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.webp *.gif)"
        )
        
        if file_paths:
            for file_path in file_paths:
                # 检查文件是否已在列表中
                if not self.is_file_in_list(list_widget, file_path):
                    list_widget.addItem(file_path)
    
    def add_directory(self, list_widget):
        """添加目录中的所有图片"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择图片目录"
        )
        
        if dir_path:
            # 支持的图片扩展名
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif']
            
            # 遍历目录，添加匹配的文件
            for root, _, files in os.walk(dir_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in extensions:
                        file_path = os.path.join(root, file)
                        # 检查文件是否已在列表中
                        if not self.is_file_in_list(list_widget, file_path):
                            list_widget.addItem(file_path)
    
    def is_file_in_list(self, list_widget, file_path):
        """检查文件是否已经在列表中"""
        for i in range(list_widget.count()):
            if list_widget.item(i).text() == file_path:
                return True
        return False
    
    def clear_files(self, list_widget):
        """清空文件列表"""
        list_widget.clear()
    
    def select_output_dir(self, line_edit):
        """选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择输出目录", line_edit.text()
        )
        
        if dir_path:
            line_edit.setText(dir_path)
    
    def set_input_file(self, file_path):
        """设置输入文件（主界面拖放支持）"""
        # 根据当前标签页添加到相应的列表
        tab_index = self.tabs.currentIndex()
        
        if tab_index == 0:  # 格式转换
            if not self.is_file_in_list(self.format_file_list, file_path):
                self.format_file_list.addItem(file_path)
        elif tab_index == 1:  # 尺寸调整
            if not self.is_file_in_list(self.resize_file_list, file_path):
                self.resize_file_list.addItem(file_path)
        elif tab_index == 2:  # 图片压缩
            if not self.is_file_in_list(self.compress_file_list, file_path):
                self.compress_file_list.addItem(file_path)
    
    def start_processing(self, operation_type):
        """开始处理图片"""
        # 根据操作类型获取相应的界面元素
        if operation_type == "format_convert":
            file_list = self.format_file_list
            output_path = self.format_output_path.text()
            progress_bar = self.format_progress
            start_button = self.format_start_button
            params = {'target_format': self.format_combo.currentText().lower()}
        elif operation_type == "resize":
            file_list = self.resize_file_list
            output_path = self.resize_output_path.text()
            progress_bar = self.resize_progress
            start_button = self.resize_start_button
            params = {
                'width': self.width_spin.value(),
                'height': self.height_spin.value(),
                'keep_aspect_ratio': self.keep_aspect_ratio.isChecked()
            }
        elif operation_type == "compress":
            file_list = self.compress_file_list
            output_path = self.compress_output_path.text()
            progress_bar = self.compress_progress
            start_button = self.compress_start_button
            params = {'quality': self.quality_spin.value()}
        else:
            return
        
        # 检查文件列表和输出目录
        if file_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加要处理的图片")
            return
        
        if not output_path:
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
        
        # 确保输出目录存在
        try:
            os.makedirs(output_path, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建输出目录失败: {str(e)}")
            return
        
        # 收集文件列表
        files = []
        for i in range(file_list.count()):
            files.append(file_list.item(i).text())
        
        # 启动处理线程
        progress_bar.setValue(0)
        start_button.setEnabled(False)
        
        self.processing_thread = ImageProcessingThread(
            self.processor, operation_type, files, output_path, params
        )
        self.processing_thread.progress_updated.connect(
            lambda value: progress_bar.setValue(value)
        )
        self.processing_thread.processing_completed.connect(
            lambda success, message, results: self.processing_finished(
                success, message, results, file_list, start_button
            )
        )
        self.processing_thread.start()
    
    def processing_finished(self, success, message, results, file_list, start_button):
        """处理完成回调"""
        start_button.setEnabled(True)
        
        if success:
            # 更新文件列表状态
            if results:
                for i, (input_path, output_path, ok, result_msg) in enumerate(results):
                    for j in range(file_list.count()):
                        if file_list.item(j).text() == input_path:
                            item = file_list.item(j)
                            if ok:
                                item.setText(f"{input_path} -> {output_path} {result_msg}")
                                item.setForeground(QColor(0, 128, 0))  # 绿色
                            else:
                                item.setText(f"{input_path} - 失败: {result_msg}")
                                item.setForeground(QColor(255, 0, 0))  # 红色
                            break
            
            QMessageBox.information(self, "处理完成", "图片处理成功！")
        else:
            QMessageBox.critical(self, "处理失败", f"错误: {message}") 