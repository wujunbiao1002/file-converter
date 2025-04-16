#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 设置窗口
版权所有 (c) 2025 Junly
"""

import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFileDialog, QComboBox, QTabWidget,
    QCheckBox, QSpinBox, QGroupBox, QRadioButton, QButtonGroup,
    QDialogButtonBox, QListWidget, QListWidgetItem, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from utils.logger import get_logger

logger = get_logger()

class SettingsWindow(QDialog):
    """设置窗口类"""
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        
        self.config = config
        self.temp_settings = {}
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle("设置")
        self.setMinimumSize(500, 400)
        
        # 主布局
        layout = QVBoxLayout()
        
        # 设置标签页
        self.tabs = QTabWidget()
        
        # 一般设置标签页
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        
        # 输出目录设置
        output_group = QGroupBox("默认输出目录")
        output_layout = QHBoxLayout()
        
        self.output_path = QLineEdit()
        output_layout.addWidget(self.output_path)
        
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(browse_button)
        
        output_group.setLayout(output_layout)
        general_layout.addWidget(output_group)
        
        # 多线程设置
        thread_group = QGroupBox("批量处理线程数")
        thread_layout = QHBoxLayout()
        
        self.thread_count = QSpinBox()
        self.thread_count.setMinimum(1)
        self.thread_count.setMaximum(16)
        thread_layout.addWidget(self.thread_count)
        
        thread_group.setLayout(thread_layout)
        general_layout.addWidget(thread_group)
        
        # 主题设置
        theme_group = QGroupBox("主题")
        theme_layout = QVBoxLayout()
        
        self.theme_light = QRadioButton("亮色主题")
        self.theme_dark = QRadioButton("暗色主题")
        self.theme_win11_light = QRadioButton("Windows 11 亮色主题")
        self.theme_win11_dark = QRadioButton("Windows 11 暗色主题")
        
        theme_layout.addWidget(self.theme_light)
        theme_layout.addWidget(self.theme_dark)
        theme_layout.addWidget(self.theme_win11_light)
        theme_layout.addWidget(self.theme_win11_dark)
        
        theme_group.setLayout(theme_layout)
        general_layout.addWidget(theme_group)
        
        # 语言设置
        lang_group = QGroupBox("语言")
        lang_layout = QHBoxLayout()
        
        self.language = QComboBox()
        self.language.addItems(["简体中文"])
        lang_layout.addWidget(self.language)
        
        lang_group.setLayout(lang_layout)
        general_layout.addWidget(lang_group)
        
        # 添加拉伸空间
        general_layout.addStretch()
        
        general_tab.setLayout(general_layout)
        
        # 最近文件标签页
        recent_tab = QWidget()
        recent_layout = QVBoxLayout()
        
        self.recent_files = QListWidget()
        recent_layout.addWidget(self.recent_files)
        
        clear_button = QPushButton("清空最近文件列表")
        clear_button.clicked.connect(self.clear_recent_files)
        recent_layout.addWidget(clear_button)
        
        recent_tab.setLayout(recent_layout)
        
        # 添加标签页到标签页控件
        self.tabs.addTab(general_tab, "常规")
        self.tabs.addTab(recent_tab, "最近文件")
        
        layout.addWidget(self.tabs)
        
        # 添加确定/取消按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """从配置加载设置"""
        # 加载输出路径
        self.output_path.setText(self.config.get("default_output_path"))
        
        # 加载线程数
        self.thread_count.setValue(self.config.get("batch_threads"))
        
        # 加载主题
        theme = self.config.get("theme")
        if theme == "light":
            self.theme_light.setChecked(True)
        elif theme == "dark":
            self.theme_dark.setChecked(True)
        elif theme == "win11_light":
            self.theme_win11_light.setChecked(True)
        elif theme == "win11_dark":
            self.theme_win11_dark.setChecked(True)
        else:
            self.theme_light.setChecked(True)
        
        # 加载语言
        if self.config.get("language") == "zh_CN":
            self.language.setCurrentIndex(0)
        else:
            self.language.setCurrentIndex(1)
        
        # 加载最近文件
        self.load_recent_files()
    
    def load_recent_files(self):
        """加载最近文件列表"""
        self.recent_files.clear()
        
        for file_path in self.config.get_recent_files():
            item = QListWidgetItem(file_path)
            self.recent_files.addItem(item)
    
    def clear_recent_files(self):
        """清空最近文件列表"""
        self.config.clear_recent_files()
        self.recent_files.clear()
    
    def browse_output_dir(self):
        """浏览选择默认输出目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择默认输出目录", self.output_path.text()
        )
        
        if dir_path:
            self.output_path.setText(dir_path)
    
    def accept(self):
        """确定按钮处理"""
        # 保存输出路径
        self.config.set("default_output_path", self.output_path.text())
        
        # 保存线程数
        self.config.set("batch_threads", self.thread_count.value())
        
        # 保存主题
        if self.theme_light.isChecked():
            self.config.set("theme", "light")
        elif self.theme_dark.isChecked():
            self.config.set("theme", "dark")
        elif self.theme_win11_light.isChecked():
            self.config.set("theme", "win11_light")
        elif self.theme_win11_dark.isChecked():
            self.config.set("theme", "win11_dark")
        
        # 保存语言
        if self.language.currentIndex() == 0:
            self.config.set("language", "zh_CN")
        else:
            self.config.set("language", "en_US")
        
        # 保存配置
        self.config.save()
        
        logger.info("保存设置成功")
        
        # 关闭对话框
        super().accept() 