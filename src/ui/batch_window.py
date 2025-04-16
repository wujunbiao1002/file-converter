#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 批量处理窗口
版权所有 (c) 2025 Junly
"""

import os
import time
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QComboBox, QListWidget, QListWidgetItem,
    QProgressBar, QGroupBox, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QColor

from utils.logger import get_logger

logger = get_logger()

class BatchProcessThread(QThread):
    """批量处理线程"""
    progress_updated = pyqtSignal(int, int)  # 参数：当前文件索引，总文件数
    file_completed = pyqtSignal(int, bool, str)  # 参数：文件索引，成功标志，消息
    all_completed = pyqtSignal()
    
    def __init__(self, converter, files, output_dir, conversion_type, options=None):
        super().__init__()
        self.converter = converter
        self.files = files
        self.output_dir = output_dir
        self.conversion_type = conversion_type
        self.options = options or {}
        self.running = True
    
    def run(self):
        """执行批量转换"""
        for i, file_path in enumerate(self.files):
            if not self.running:
                break
                
            try:
                # 根据文件类型和转换类型，分发到不同的处理方法
                result = self.process_file(file_path, i)
                
                # 发送完成信号
                if result:
                    self.file_completed.emit(i, True, "成功")
                else:
                    self.file_completed.emit(i, False, "处理失败")
                    
            except Exception as e:
                logger.exception(f"处理文件失败: {file_path}")
                self.file_completed.emit(i, False, str(e))
            
            # 更新进度
            self.progress_updated.emit(i + 1, len(self.files))
        
        self.all_completed.emit()
    
    def process_file(self, file_path, index):
        """处理单个文件"""
        # 获取文件基本信息
        file_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        # 根据转换类型确定输出文件扩展名
        output_ext = self.get_output_extension()
        
        # 构建输出文件路径
        output_path = os.path.join(self.output_dir, f"{name_without_ext}{output_ext}")
        
        # 调用对应的转换方法
        return self.call_converter_method(file_path, output_path)
    
    def get_output_extension(self):
        """根据转换类型获取输出文件扩展名"""
        # 根据转换类型返回相应的扩展名
        conversion_map = {
            "word_to_markdown": ".md",
            "word_to_html": ".html",
            "word_remove_images": ".docx",
            "word_to_text": ".txt",
            "excel_to_txt": ".txt",
            "excel_to_markdown": ".md",
            "markdown_to_word": ".docx",
            "markdown_tables_to_excel": ".xlsx",
            "pdf_to_word": ".docx",
            "pdf_to_text": ".txt",
            "pdf_extract_images": "",  # 将创建一个图片目录
            "image_format_convert": "",  # 根据目标格式确定
            "image_resize": "",  # 保持原格式
            "image_compress": "",  # 保持原格式
            "text_encoding_convert": ".txt",
            "text_to_html": ".html",
            "text_to_markdown": ".md",
            "text_batch_replace": ".txt"
        }
        
        return conversion_map.get(self.conversion_type, "")
    
    def call_converter_method(self, input_path, output_path):
        """调用转换器的对应方法"""
        # 这里需要根据转换类型调用不同的转换方法
        
        # 文本处理功能
        if self.conversion_type == "text_encoding_convert":
            # 编码转换
            target_encoding = self.options.get("target_encoding", "UTF-8")
            result = self.converter.convert_encoding(input_path, output_path, target_encoding)
            return result
            
        elif self.conversion_type == "text_to_html":
            # 转换为HTML
            result = self.converter.text_to_html(input_path, output_path)
            return result
            
        elif self.conversion_type == "text_to_markdown":
            # 转换为Markdown
            result = self.converter.text_to_markdown(input_path, output_path)
            return result
            
        elif self.conversion_type == "text_batch_replace":
            # 批量替换
            # 使用之前设置的替换规则
            if not hasattr(self.converter, "replace_rules") or not self.converter.replace_rules:
                # 如果没有设置替换规则，尝试从选项中获取并设置
                rules_text = self.options.get("replace_rules", "")
                if rules_text:
                    self.converter.set_replace_rules(rules_text)
                else:
                    logger.error("未设置替换规则")
                    return False
                    
            result = self.converter.batch_replace(input_path, output_path)
            return result
            
        # Word转换功能
        elif self.conversion_type == "word_to_markdown":
            # 读取文档
            doc = self.converter.read_word(input_path)
            # 转换为Markdown
            result = self.converter.save_as_markdown(
                doc, output_path, 
                self.options.get("include_images", True)
            )
            return result
            
        elif self.conversion_type == "word_to_html":
            # 读取文档
            doc = self.converter.read_word(input_path)
            # 转换为HTML
            result = self.converter.save_as_html(
                doc, output_path,
                self.options.get("include_images", True)
            )
            return result
            
        elif self.conversion_type == "word_remove_images":
            # 移除图片
            result = self.converter.remove_images(input_path, output_path)
            return result
            
        elif self.conversion_type == "word_to_text":
            # 读取文档
            doc = self.converter.read_word(input_path)
            # 转换为文本
            result = self.converter.save_as_text(doc, output_path)
            return result
            
        # 其他转换类型暂未实现
        logger.warning(f"未实现的转换类型: {self.conversion_type}")
        return False
    
    def stop(self):
        """停止处理"""
        self.running = False

class BatchWindow(QDialog):
    """批量处理窗口"""
    
    def __init__(self, converter, conversion_type, config, parent=None):
        super().__init__(parent)
        
        self.converter = converter  # 转换器对象
        self.conversion_type = conversion_type  # 转换类型
        self.config = config  # 配置对象
        self.files = []  # 要处理的文件列表
        self.output_directory = ""  # 输出目录
        self.options = {}  # 处理选项
        
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle("批量处理")
        self.setMinimumSize(600, 500)
        
        # 主布局
        layout = QVBoxLayout()
        
        # 文件列表区域
        file_group = QGroupBox("待处理文件")
        file_layout = QVBoxLayout()
        
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list)
        
        file_buttons = QHBoxLayout()
        
        add_files_button = QPushButton("添加文件")
        add_files_button.clicked.connect(self.add_files)
        file_buttons.addWidget(add_files_button)
        
        add_dir_button = QPushButton("添加目录")
        add_dir_button.clicked.connect(self.add_directory)
        file_buttons.addWidget(add_dir_button)
        
        clear_button = QPushButton("清空列表")
        clear_button.clicked.connect(self.clear_files)
        file_buttons.addWidget(clear_button)
        
        file_layout.addLayout(file_buttons)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # 输出目录区域
        output_group = QGroupBox("输出目录")
        output_layout = QHBoxLayout()
        
        self.output_path = QLineEdit()
        self.output_path.setText(self.config.get("default_output_path"))
        self.output_path.setReadOnly(True)
        output_layout.addWidget(self.output_path)
        
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(browse_button)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # 进度区域
        progress_group = QGroupBox("处理进度")
        progress_layout = QVBoxLayout()
        
        self.progress_label = QLabel("准备就绪")
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        
        self.file_status = QListWidget()
        self.file_status.setMinimumHeight(150)
        progress_layout.addWidget(self.file_status)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.start_button = QPushButton("开始处理")
        self.start_button.clicked.connect(self.start_processing)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("停止")
        self.stop_button.clicked.connect(self.stop_processing)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def setOptions(self, options):
        """设置处理选项
        
        Args:
            options (dict): 处理选项字典
        """
        self.options = options or {}

    def add_files(self):
        """添加文件到处理列表"""
        # 根据转换类型获取文件过滤器
        file_filter = self.get_file_filter()
        
        # 打开文件选择对话框
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择文件", "", file_filter
        )
        
        # 添加文件到列表
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
                self.file_list.addItem(file_path)
                
        # 更新开始按钮状态
        self.start_button.setEnabled(len(self.files) > 0 and bool(self.output_path.text()))
    
    def add_directory(self):
        """添加目录中的所有符合条件的文件"""
        # 选择目录
        directory = QFileDialog.getExistingDirectory(
            self, "选择目录", ""
        )
        
        if not directory:
            return
            
        # 获取支持的文件扩展名
        extensions = self.get_file_extensions()
        
        # 递归遍历目录，添加所有符合条件的文件
        added_count = 0
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in extensions and file_path not in self.files:
                    self.files.append(file_path)
                    self.file_list.addItem(file_path)
                    added_count += 1
                    
        # 提示添加结果
        if added_count > 0:
            QMessageBox.information(self, "添加完成", f"已添加{added_count}个文件")
        else:
            QMessageBox.warning(self, "添加失败", "目录中没有符合条件的文件")
            
        # 更新开始按钮状态
        self.start_button.setEnabled(len(self.files) > 0 and bool(self.output_path.text()))
    
    def clear_files(self):
        """清空文件列表"""
        self.files = []
        self.file_list.clear()
        self.start_button.setEnabled(False)
    
    def browse_output_dir(self):
        """浏览输出目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择输出目录", self.output_path.text()
        )
        
        if directory:
            self.output_path.setText(directory)
            self.output_directory = directory
            
            # 更新开始按钮状态
            self.start_button.setEnabled(len(self.files) > 0)
    
    def get_file_filter(self):
        """根据转换类型获取文件过滤器"""
        # 根据不同的转换类型返回相应的文件过滤器
        conversion_map = {
            "word_to_markdown": "Word文档 (*.docx *.doc)",
            "word_to_html": "Word文档 (*.docx *.doc)",
            "word_remove_images": "Word文档 (*.docx *.doc)",
            "word_to_text": "Word文档 (*.docx *.doc)",
            "excel_to_txt": "Excel文档 (*.xlsx *.xls)",
            "excel_to_markdown": "Excel文档 (*.xlsx *.xls)",
            "markdown_to_word": "Markdown文档 (*.md)",
            "markdown_tables_to_excel": "Markdown文档 (*.md)",
            "pdf_to_word": "PDF文档 (*.pdf)",
            "pdf_to_text": "PDF文档 (*.pdf)",
            "pdf_extract_images": "PDF文档 (*.pdf)",
            "image_format_convert": "图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff)",
            "image_resize": "图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff)",
            "image_compress": "图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff)",
            "text_encoding_convert": "文本文件 (*.txt);;所有文件 (*)",
            "text_to_html": "文本文件 (*.txt);;所有文件 (*)",
            "text_to_markdown": "文本文件 (*.txt);;所有文件 (*)",
            "text_batch_replace": "文本文件 (*.txt);;所有文件 (*)"
        }
        
        return conversion_map.get(self.conversion_type, "所有文件 (*)")
    
    def get_file_extensions(self):
        """根据转换类型获取支持的文件扩展名"""
        # 根据不同的转换类型返回相应的文件扩展名列表
        conversion_map = {
            "word_to_markdown": [".docx", ".doc"],
            "word_to_html": [".docx", ".doc"],
            "word_remove_images": [".docx", ".doc"],
            "word_to_text": [".docx", ".doc"],
            "excel_to_txt": [".xlsx", ".xls"],
            "excel_to_markdown": [".xlsx", ".xls"],
            "markdown_to_word": [".md"],
            "markdown_tables_to_excel": [".md"],
            "pdf_to_word": [".pdf"],
            "pdf_to_text": [".pdf"],
            "pdf_extract_images": [".pdf"],
            "image_format_convert": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
            "image_resize": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
            "image_compress": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
            "text_encoding_convert": [".txt"],
            "text_to_html": [".txt"],
            "text_to_markdown": [".txt"],
            "text_batch_replace": [".txt"]
        }
        
        return conversion_map.get(self.conversion_type, [])
    
    def start_processing(self):
        """开始批量处理"""
        # 检查文件列表和输出目录
        if not self.files:
            QMessageBox.warning(self, "警告", "请先添加文件")
            return
            
        if not self.output_path.text():
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
            
        # 确保输出目录存在
        output_dir = self.output_path.text()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建输出目录失败: {str(e)}")
                return
                
        # 清空状态列表
        self.file_status.clear()
        
        # 准备进度条
        self.progress_bar.setMaximum(len(self.files))
        self.progress_bar.setValue(0)
        
        # 更新UI状态
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.close_button.setEnabled(False)
        
        # 创建并启动处理线程
        self.process_thread = BatchProcessThread(
            self.converter,
            self.files,
            output_dir,
            self.conversion_type,
            self.options
        )
        
        # 连接信号
        self.process_thread.progress_updated.connect(self.update_progress)
        self.process_thread.file_completed.connect(self.file_completed)
        self.process_thread.all_completed.connect(self.processing_completed)
        
        # 开始处理
        self.process_thread.start()
        
        # 更新状态
        self.progress_label.setText("正在处理...")
    
    def stop_processing(self):
        """停止处理"""
        if hasattr(self, 'process_thread') and self.process_thread and self.process_thread.isRunning():
            self.status_label.setText("正在停止...")
            self.process_thread.stop()
            
            # 等待线程结束
            if not self.process_thread.wait(3000):  # 等待最多3秒
                self.status_label.setText("线程无响应，强制停止")
                # 如果线程没有响应，则记录警告
                logger.warning("批处理线程未响应停止请求，可能需要强制终止")
            else:
                self.status_label.setText("已停止")
            
            # 重置UI
            self.start_button.setEnabled(True)
            self.start_button.setText("开始处理")
            self.stop_button.setEnabled(False)
            
            # 确认进度重置
            self.progress_bar.setValue(0)
    
    def update_progress(self, current, total):
        """更新进度条
        
        Args:
            current (int): 当前已处理文件数
            total (int): 总文件数
        """
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"正在处理... ({current}/{total})")
    
    def file_completed(self, index, success, message):
        """文件处理完成回调
        
        Args:
            index (int): 文件索引
            success (bool): 是否成功
            message (str): 状态消息
        """
        # 获取文件路径
        file_path = self.files[index]
        file_name = os.path.basename(file_path)
        
        # 创建状态项
        item_text = f"{file_name}: {'成功' if success else '失败 - ' + message}"
        item = QListWidgetItem(item_text)
        
        # 设置状态项颜色
        if success:
            item.setData(Qt.ItemDataRole.ForegroundRole, QColor(0, 180, 0))  # 绿色
        else:
            item.setData(Qt.ItemDataRole.ForegroundRole, QColor(255, 0, 0))  # 红色
            
        # 添加到状态列表
        self.file_status.addItem(item)
        self.file_status.scrollToBottom()
        
        # 强制刷新视图以确保颜色正确显示
        self.file_status.repaint()
    
    def processing_completed(self):
        """所有文件处理完成"""
        # 更新UI状态
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.close_button.setEnabled(True)
        
        # 更新状态
        self.progress_label.setText("处理完成")
        
        # 弹出完成提示
        QMessageBox.information(self, "完成", "批量处理已完成")
    
    def closeEvent(self, event):
        """关闭窗口前确认停止所有处理"""
        if hasattr(self, 'process_thread') and self.process_thread and self.process_thread.isRunning():
            # 尝试优雅地停止线程
            logger.info("窗口关闭中，正在停止批处理线程...")
            self.process_thread.stop()
            
            # 等待线程终止
            if not self.process_thread.wait(2000):  # 等待最多2秒
                logger.warning("批处理线程未能在窗口关闭前终止")
            else:
                logger.info("批处理线程已成功停止")
        
        # 调用父类的closeEvent
        super().closeEvent(event) 