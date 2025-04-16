#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - Windows 11风格主题
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
}

QMenuBar {
    background-color: transparent;
    spacing: 2px;
    padding: 4px 0px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #f0f0f0;
}

QMenuBar::item:pressed {
    background-color: #e5e5e5;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 4px 0px;
}

QMenu::item {
    padding: 6px 30px 6px 20px;
}

QMenu::item:selected {
    background-color: #f0f0f0;
    border-radius: 4px;
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

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #0067c0;
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
    background-color: transparent;
    spacing: 2px;
    padding: 4px 0px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 8px;
    border-radius: 4px;
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
}

QMenu::item {
    padding: 6px 30px 6px 20px;
}

QMenu::item:selected {
    background-color: #3a3a3a;
    border-radius: 4px;
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

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #0078d4;
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
""" 