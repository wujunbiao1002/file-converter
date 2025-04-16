#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件工具 - Windows 11风格主题
版权所有 (c) 2025 Junly
"""

# Windows 11风格的浅色主题样式表
WIN11_LIGHT_STYLE = """
QMainWindow, QDialog {
    background-color: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}

QWidget {
    font-family: 'Segoe UI', 'Microsoft YaHei UI';
    font-size: 10pt;
    color: #000000;
}

QMenuBar {
    background-color: #f5f5f5;
    spacing: 2px;
    padding: 4px 0px;
    border-bottom: 1px solid #e0e0e0;
}

QMenuBar::item {
    background-color: transparent;
    padding: 6px 10px;
    border-radius: 4px;
    margin: 1px 2px;
}

QMenuBar::item:selected {
    background-color: #e5e5e5;
}

QMenuBar::item:pressed {
    background-color: #d0d0d0;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 4px 0px;
    margin: 2px;
}

QMenu::item {
    padding: 6px 30px 6px 20px;
    background-color: transparent;
    border-radius: 4px;
    margin: 2px 4px;
}

QMenu::item:selected {
    background-color: #e5f1fb;
    color: #000000;
}

QMenu::separator {
    height: 1px;
    background-color: #e0e0e0;
    margin: 4px 10px;
}

QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 6px 16px;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #e5e5e5;
}

QPushButton:pressed {
    background-color: #d0d0d0;
}

QPushButton:focus {
    border: 1px solid #0067c0;
}

QPushButton:default {
    background-color: #0067c0;
    color: white;
    border: none;
}

QPushButton:default:hover {
    background-color: #0078d4;
}

QPushButton:default:pressed {
    background-color: #005a9e;
}

QTabWidget::pane {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    top: -1px;
}

QTabBar::tab {
    background-color: transparent;
    border-bottom: 2px solid transparent;
    padding: 8px 16px;
}

QTabBar::tab:selected {
    border-bottom: 2px solid #0067c0;
    color: #0067c0;
}

QTabBar::tab:hover:!selected {
    border-bottom: 2px solid #c0c0c0;
}

QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 6px 8px;
    min-height: 24px;
}

QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QSpinBox:hover {
    border: 1px solid #c0c0c0;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #0067c0;
    background-color: #f9f9f9;
}

QProgressBar {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    text-align: center;
    background-color: #f0f0f0;
}

QProgressBar::chunk {
    background-color: #0067c0;
    border-radius: 5px;
}

QStatusBar {
    background-color: #f5f5f5;
    color: #666666;
}

QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #c0c0c0;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #a0a0a0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #c0c0c0;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #a0a0a0;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QHeaderView::section {
    background-color: #f5f5f5;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #e0e0e0;
}

QTableView {
    gridline-color: #f0f0f0;
    selection-background-color: #e5f1fb;
    selection-color: #000000;
}

QCheckBox {
    spacing: 8px;
    color: #000000;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #c0c0c0;
    border-radius: 3px;
    background: #ffffff;
}

QCheckBox::indicator:hover {
    border: 1px solid #0067c0;
}

QCheckBox::indicator:checked {
    background-color: #0067c0;
    border: 1px solid #0067c0;
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDE0IDE0Ij48cGF0aCBmaWxsPSIjZmZmZmZmIiBkPSJNMTEuNDI4NiAzLjc3MzE4QzExLjIxODkgMy41NDc0NCAxMC44NzcxIDMuNTMxOTkgMTAuNjUwMyAzLjczOTczTDUuMzI0NzcgOC42MjkzMkwzLjM0OTcyIDYuNDcxOTJDMy4xNDEwOSA2LjI0Mzk3IDIuNzk5MTYgNi4yMjgzMSAyLjU3MTIyIDYuNDM2OTRDMi4zNDMyNyA2LjY0NTU3IDIuMzI3NjEgNi45ODc1IDIuNTM2MjQgNy4yMTU0NUw0Ljk4MTIzIDkuOTExODVDNS4wODE4NyAxMC4wMjI5IDUuMjE5NCAxMC4wODUzIDUuMzY0NzMgMTAuMDg1M0M1LjQ5Mzg1IDEwLjA4NTMgNS42MTk0MSAxMC4wMzQyIDUuNzE3ODUgOS45NDE0MUwxMS40OTExIDQuNTQ3OTNDMTE4NzE3OSA0LjM0MDIgMTEuNzMzNSAzLjk5ODI3IDExLjUyNTggMy43NzAzM1YzLjc3MzE4WiIvPjwvc3ZnPg==);
}

QCheckBox::indicator:checked:disabled {
    background-color: #c0c0c0;
    border: 1px solid #c0c0c0;
}

QRadioButton {
    spacing: 8px;
    color: #000000;
    padding: 2px;
}

QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border: 1px solid #c0c0c0;
    border-radius: 10px;
    background-color: #ffffff;
}

QRadioButton::indicator:hover {
    border: 1px solid #0067c0;
}

QRadioButton::indicator:unchecked {
    background-color: #ffffff;
    image: none;
}

QRadioButton::indicator:checked {
    background-color: #ffffff;
    border: 1px solid #0067c0;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI2IiBjeT0iNiIgcj0iNiIgZmlsbD0iIzAwNjdjMCIvPjwvc3ZnPg==);
}

QRadioButton::indicator:checked:disabled {
    background-color: #e0e0e0;
    border: 1px solid #c0c0c0;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI2IiBjeT0iNiIgcj0iNiIgZmlsbD0iI2MwYzBjMCIvPjwvc3ZnPg==);
}

/* 添加下拉框相关样式 */
QComboBox {
    padding-right: 20px; /* 为下拉箭头留出空间 */
    color: #000000; /* 确保主内容文字颜色为黑色 */
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 4px 8px;
    padding-right: 20px;
    min-height: 24px;
}

QComboBox:hover {
    border: 1px solid #c0c0c0;
}

QComboBox:focus {
    border: 1px solid #0067c0;
}

QComboBox:disabled {
    color: #888888;
    background-color: #f5f5f5;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 20px;
    border-left: none;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QComboBox::down-arrow {
    image: none;
    width: 12px;
    height: 12px;
}

QComboBox::down-arrow:before {
    content: "▼";
    color: #555555;
    font-size: 8pt;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    selection-background-color: #e5f1fb;
    selection-color: #000000;
    color: #000000;  /* 设置下拉列表项文字颜色 */
    outline: 0px;   /* 移除焦点边框 */
}

QComboBox QAbstractItemView::item {
    min-height: 24px;
    padding: 2px 10px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #f0f0f0;
    border-radius: 4px;
}

/* 添加QListWidget样式 */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 2px;
    outline: none;
    selection-background-color: #e5f1fb;
    selection-color: #000000;
}

QListWidget::item {
    min-height: 24px;
    padding: 4px 8px;
    border-radius: 4px;
    margin: 2px;
    /* 允许项目使用自定义文本颜色 */
    color: -1; /* 使用-1表示继承/自动，这样可以允许通过setForeground设置的颜色显示 */
}

QListWidget::item:selected {
    background-color: #e5f1fb;
    /* 选中时仍保留自定义颜色设置 */
    color: -1;  /* 使用-1表示继承/自动 */
    border: 1px solid #0067c0;
}

QListWidget::item:hover:!selected {
    background-color: #f0f0f0;
    border: 1px solid #e0e0e0;
}

/* 添加QGroupBox样式 */
QGroupBox {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    margin-top: 24px;
    font-weight: bold;
    background-color: #f9f9f9;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    background-color: #f9f9f9;
}
"""

# Windows 11风格的深色主题样式表
WIN11_DARK_STYLE = """
QMainWindow, QDialog {
    background-color: #202020;
    border: 1px solid #303030;
    border-radius: 8px;
}

QWidget {
    font-family: 'Segoe UI', 'Microsoft YaHei UI';
    font-size: 10pt;
    color: #ffffff;
}

QMenuBar {
    background-color: #202020;
    spacing: 2px;
    padding: 4px 0px;
    border-bottom: 1px solid #303030;
}

QMenuBar::item {
    background-color: transparent;
    padding: 6px 10px;
    border-radius: 4px;
    margin: 1px 2px;
}

QMenuBar::item:selected {
    background-color: #3a3a3a;
}

QMenuBar::item:pressed {
    background-color: #444444;
}

QMenu {
    background-color: #2c2c2c;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    padding: 4px 0px;
    margin: 2px;
}

QMenu::item {
    padding: 6px 30px 6px 20px;
    background-color: transparent;
    border-radius: 4px;
    margin: 2px 4px;
}

QMenu::item:selected {
    background-color: #2c5c94;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background-color: #3a3a3a;
    margin: 4px 10px;
}

QPushButton {
    background-color: #323232;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 6px 16px;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #3a3a3a;
}

QPushButton:pressed {
    background-color: #444444;
}

QPushButton:focus {
    border: 1px solid #0078d4;
}

QPushButton:default {
    background-color: #0078d4;
    color: white;
    border: none;
}

QPushButton:default:hover {
    background-color: #1a86d9;
}

QPushButton:default:pressed {
    background-color: #006cbe;
}

QTabWidget::pane {
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    top: -1px;
}

QTabBar::tab {
    background-color: transparent;
    border-bottom: 2px solid transparent;
    padding: 8px 16px;
}

QTabBar::tab:selected {
    border-bottom: 2px solid #0078d4;
    color: #0078d4;
}

QTabBar::tab:hover:!selected {
    border-bottom: 2px solid #505050;
}

QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #2c2c2c;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px 8px;
    min-height: 24px;
}

QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QSpinBox:hover {
    border: 1px solid #505050;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #0078d4;
    background-color: #323232;
}

QProgressBar {
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    text-align: center;
    background-color: #323232;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 5px;
}

QStatusBar {
    background-color: #202020;
    color: #b0b0b0;
}

QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #505050;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #606060;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 10px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #505050;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: #606060;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QHeaderView::section {
    background-color: #2c2c2c;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #3a3a3a;
}

QTableView {
    gridline-color: #3a3a3a;
    selection-background-color: #2c5c94;
    selection-color: #ffffff;
}

QCheckBox {
    spacing: 8px;
    color: #ffffff;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #505050;
    border-radius: 3px;
    background: #2c2c2c;
}

QCheckBox::indicator:hover {
    border: 1px solid #0078d4;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border: 1px solid #0078d4;
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDE0IDE0Ij48cGF0aCBmaWxsPSIjZmZmZmZmIiBkPSJNMTEuNDI4NiAzLjc3MzE4QzExLjIxODkgMy41NDc0NCAxMC44NzcxIDMuNTMxOTkgMTAuNjUwMyAzLjczOTczTDUuMzI0NzcgOC42MjkzMkwzLjM0OTcyIDYuNDcxOTJDMy4xNDEwOSA2LjI0Mzk3IDIuNzk5MTYgNi4yMjgzMSAyLjU3MTIyIDYuNDM2OTRDMi4zNDMyNyA2LjY0NTU3IDIuMzI3NjEgNi45ODc1IDIuNTM2MjQgNy4yMTU0NUw0Ljk4MTIzIDkuOTExODVDNS4wODE4NyAxMC4wMjI5IDUuMjE5NCAxMC4wODUzIDUuMzY0NzMgMTAuMDg1M0M1LjQ5Mzg1IDEwLjA4NTMgNS42MTk0MSAxMC4wMzQyIDUuNzE3ODUgOS45NDE0MUwxMS40OTExIDQuNTQ3OTNDMTE3MTc5IDQuMzQwMiAxMS43MzM1IDMuOTk4MjcgMTEuNTI1OCAzLjc3MDMzVjMuNzczMThaIi8+PC9zdmc+);
}

QCheckBox::indicator:checked:disabled {
    background-color: #505050;
    border: 1px solid #505050;
}

QRadioButton {
    spacing: 8px;
    color: #ffffff;
    padding: 2px;
}

QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border: 1px solid #505050;
    border-radius: 10px;
    background-color: #2c2c2c;
}

QRadioButton::indicator:hover {
    border: 1px solid #0078d4;
}

QRadioButton::indicator:unchecked {
    background-color: #2c2c2c;
    image: none;
}

QRadioButton::indicator:checked {
    background-color: #2c2c2c;
    border: 1px solid #0078d4;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI2IiBjeT0iNiIgcj0iNiIgZmlsbD0iIzAwNzhkNCIvPjwvc3ZnPg==);
}

QRadioButton::indicator:checked:disabled {
    background-color: #323232;
    border: 1px solid #505050;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI2IiBjeT0iNiIgcj0iNiIgZmlsbD0iIzUwNTA1MCIvPjwvc3ZnPg==);
}

/* 添加下拉框相关样式 */
QComboBox {
    padding-right: 20px; /* 为下拉箭头留出空间 */
    color: #ffffff; /* 确保主内容文字颜色为白色 */
    background-color: #2c2c2c;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 4px 8px;
    padding-right: 20px;
    min-height: 24px;
}

QComboBox:hover {
    border: 1px solid #505050;
}

QComboBox:focus {
    border: 1px solid #0078d4;
}

QComboBox:disabled {
    color: #888888;
    background-color: #252525;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 20px;
    border-left: none;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}

QComboBox::down-arrow {
    image: none;
    width: 12px;
    height: 12px;
}

QComboBox::down-arrow:before {
    content: "▼";
    color: #cccccc;
    font-size: 8pt;
}

QComboBox QAbstractItemView {
    background-color: #2c2c2c;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    selection-background-color: #2c5c94;
    selection-color: #ffffff;
    color: #ffffff;  /* 设置下拉列表项文字颜色 */
    outline: 0px;   /* 移除焦点边框 */
}

QComboBox QAbstractItemView::item {
    min-height: 24px;
    padding: 2px 10px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #3a3a3a;
    border-radius: 4px;
}

/* 添加QListWidget样式 */
QListWidget {
    background-color: #2c2c2c;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 2px;
    outline: none;
    selection-background-color: #2c5c94;
    selection-color: #ffffff;
}

QListWidget::item {
    min-height: 24px;
    padding: 4px 8px;
    border-radius: 4px;
    margin: 2px;
    /* 允许项目使用自定义文本颜色 */
    color: -1; /* 使用-1表示继承/自动，这样可以允许通过setForeground设置的颜色显示 */
}

QListWidget::item:selected {
    background-color: #2c5c94;
    /* 选中时仍保留自定义颜色设置 */
    color: -1; /* 使用-1表示继承/自动 */
    border: 1px solid #0078d4;
}

QListWidget::item:hover:!selected {
    background-color: #3a3a3a;
    border: 1px solid #505050;
}

/* 添加QGroupBox样式 */
QGroupBox {
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    margin-top: 24px;
    font-weight: bold;
    background-color: #262626;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    background-color: #262626;
}
""" 