#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件转换工具 - Word标签页
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
from core.word.word_converter import WordConverter

class WordConversionThread(QThread):
    """Word转换线程"""
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
                    if self.conversion_type == "markdown":
                        ext = ".md"
                    elif self.conversion_type == "html":
                        ext = ".html"
                    elif self.conversion_type == "text":
                        ext = ".txt"
                    elif self.conversion_type == "remove_images":
                        ext = ".docx"
                    else:
                        ext = ".docx"
                    
                    output_path = os.path.join(self.output_dir, f"{name_without_ext}{ext}")
                    
                    # 根据转换类型选择不同的转换方法
                    if self.conversion_type == "markdown":
                        doc = self.converter.read_word(input_file)
                        result = self.converter.save_as_markdown(
                            doc, output_path, True,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.conversion_type == "html":
                        doc = self.converter.read_word(input_file)
                        result = self.converter.save_as_html(
                            doc, output_path, True,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.conversion_type == "text":
                        doc = self.converter.read_word(input_file)
                        result = self.converter.save_as_text(
                            doc, output_path,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    elif self.conversion_type == "remove_images":
                        result = self.converter.remove_images(
                            input_file, output_path,
                            progress_callback=lambda value: self.progress_updated.emit(value)
                        )
                        results.append((input_file, output_path, True, ""))
                    else:
                        results.append((input_file, "", False, f"不支持的转换类型: {self.conversion_type}"))
                except Exception as e:
                    import traceback
                    error_details = traceback.format_exc()
                    print(f"处理文件 {input_file} 失败: {error_details}")
                    results.append((input_file, "", False, str(e)))
                
                # 更新进度
                if self.running:
                    self.progress_updated.emit(int((i+1) / len(self.input_files) * 100))
            
            if self.running:
                self.conversion_completed.emit(True, "转换成功", results)
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"转换线程出现严重错误: {error_details}")
            if self.running:
                self.conversion_completed.emit(False, str(e), None)
    
    def stop(self):
        """停止转换操作"""
        self.running = False

class WordTab(QWidget):
    """Word转换标签页"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.input_file = ""
        self.converter = WordConverter()
        self.conversion_thread = None
        self.step1_thread = None
        self.step2_thread = None
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
            "Word去除图片",
            "Word去图片转Markdown", 
            "Word去图片转HTML",
            "Word去图片转文本"
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
        """添加Word文件到处理列表"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择Word文档", "", "Word文档 (*.docx *.doc)"
        )
        
        if file_paths:
            for file_path in file_paths:
                # 检查文件是否已在列表中
                if not self.is_file_in_list(file_path):
                    self.file_list.addItem(file_path)
    
    def add_directory(self):
        """添加目录中的所有Word文件"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择Word文档目录"
        )
        
        if dir_path:
            # 支持的Word文档扩展名
            extensions = ['.docx', '.doc']
            
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
        # 选择目录
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择输出目录", self.output_path.text()
        )
        
        if dir_path:
            self.output_path.setText(dir_path)
    
    def update_output_extension(self):
        """根据转换类型更新输出文件扩展名"""
        # 批量模式不需要此功能
        pass
    
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
        if conversion_index == 0:  # Word去除图片
            conversion_type = "remove_images"
        elif conversion_index == 1:  # Word去图片转Markdown
            # 先移除图片保存到临时文件，然后转换
            temp_dir = os.path.join(output_dir, "_temp")
            self.process_remove_then_convert(input_files, temp_dir, "markdown")
            return
        elif conversion_index == 2:  # Word去图片转HTML
            # 先移除图片保存到临时文件，然后转换
            temp_dir = os.path.join(output_dir, "_temp")
            self.process_remove_then_convert(input_files, temp_dir, "html")
            return
        elif conversion_index == 3:  # Word去图片转文本
            # 先移除图片保存到临时文件，然后转换
            temp_dir = os.path.join(output_dir, "_temp")
            self.process_remove_then_convert(input_files, temp_dir, "text")
            return
        else:
            QMessageBox.warning(self, "警告", "请选择转换类型")
            return
        
        # 启动转换线程
        self.progress_bar.setValue(0)
        self.convert_button.setEnabled(False)
        
        self.conversion_thread = WordConversionThread(
            self.converter, input_files, output_dir, conversion_type
        )
        self.conversion_thread.progress_updated.connect(self.update_progress)
        self.conversion_thread.conversion_completed.connect(self.conversion_finished)
        self.conversion_thread.start()

    def process_remove_then_convert(self, files, temp_dir, final_type):
        """先去除图片，再进行转换"""
        # 确保临时目录存在
        if not os.path.exists(temp_dir):
            try:
                os.makedirs(temp_dir)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建临时目录失败: {str(e)}")
                return
        
        # 第一步：去除图片
        self.progress_bar.setValue(0)
        self.convert_button.setEnabled(False)
        
        # 如果存在以前的线程，确保它已停止
        if hasattr(self, 'step1_thread') and self.step1_thread and self.step1_thread.isRunning():
            self.step1_thread.stop()
            self.step1_thread.wait()
        
        # 创建并启动第一步转换线程
        self.step1_thread = WordConversionThread(
            self.converter, files, temp_dir, "remove_images"
        )
        self.step1_thread.progress_updated.connect(self.update_progress)
        self.step1_thread.conversion_completed.connect(
            lambda success, message, results: 
            self.step1_batch_completed(success, message, results, temp_dir, 
                                      os.path.dirname(temp_dir), final_type)
        )
        self.step1_thread.start()

    def step1_batch_completed(self, success, message, results, temp_dir, output_dir, final_type):
        """第一步批处理完成后的回调"""
        print(f"第一步处理完成: 成功={success}, 消息={message}, 结果数量={len(results) if results else 0}")
        
        if not success:
            self.convert_button.setEnabled(True)
            QMessageBox.critical(self, "转换失败", f"去除图片步骤失败: {message}")
            return
        
        # 获取成功处理的临时文件路径
        temp_files = []
        for input_path, output_path, status, error in results:
            if status and output_path:
                temp_files.append(output_path)
            else:
                print(f"文件 {input_path} 处理失败: {error}")
        
        if not temp_files:
            self.convert_button.setEnabled(True)
            QMessageBox.warning(self, "警告", "没有成功去除图片的文件，无法继续转换")
            return
        
        # 第二步：根据最终类型进行转换
        # 如果存在以前的线程，确保它已停止
        if hasattr(self, 'step2_thread') and self.step2_thread and self.step2_thread.isRunning():
            self.step2_thread.stop()
            self.step2_thread.wait()
        
        print(f"开始第二步处理: 文件数量={len(temp_files)}, 类型={final_type}")
        self.step2_thread = WordConversionThread(
            self.converter, temp_files, output_dir, final_type
        )
        self.step2_thread.progress_updated.connect(self.update_progress)
        self.step2_thread.conversion_completed.connect(
            lambda success, message, results: 
            self.step2_batch_completed(success, message, results, temp_dir)
        )
        self.step2_thread.start()
    
    def step2_batch_completed(self, success, message, results, temp_dir):
        """第二步批处理完成后的回调"""
        self.convert_button.setEnabled(True)
        
        # 清理临时文件
        try:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"临时目录 {temp_dir} 已清理")
        except Exception as e:
            print(f"清理临时文件失败: {str(e)}")  # 记录但不影响用户体验
        
        # 显示最终结果
        self.conversion_finished(success, message, results)
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def conversion_finished(self, success, message, results):
        """转换完成处理"""
        self.convert_button.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "转换完成", "文件转换成功！")
        else:
            QMessageBox.critical(self, "转换失败", f"错误: {message}")

    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 确保所有线程在窗口关闭时停止
        for thread_attr in ['conversion_thread', 'step1_thread', 'step2_thread']:
            if hasattr(self, thread_attr):
                thread = getattr(self, thread_attr)
                if thread and thread.isRunning():
                    thread.stop()
                    thread.wait()
        super().closeEvent(event) 