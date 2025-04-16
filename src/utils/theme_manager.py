#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 主题管理工具
版权所有 (c) 2025 Junly
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QEvent, QTimer
from ui.themes.win11_theme import WIN11_LIGHT_STYLE, WIN11_DARK_STYLE

class ThemeManager:
    """主题管理类"""
    
    @staticmethod
    def apply_theme(app, theme_name):
        """应用主题到应用程序
        
        Args:
            app: QApplication实例
            theme_name: 主题名称 ('light', 'dark', 'win11_light', 'win11_dark')
        """
        if theme_name == "dark":
            ThemeManager.apply_dark_theme(app)
        elif theme_name == "win11_light":
            ThemeManager.apply_win11_light_theme(app)
        elif theme_name == "win11_dark":
            ThemeManager.apply_win11_dark_theme(app)
        else:
            ThemeManager.apply_light_theme(app)
    
    @staticmethod
    def apply_light_theme(app):
        """应用亮色主题"""
        app.setStyle("Fusion")
        palette = QPalette()
        app.setPalette(palette)  # 使用默认调色板
        app.setStyleSheet("")  # 清除所有样式表
    
    @staticmethod
    def apply_dark_theme(app):
        """应用暗色主题"""
        app.setStyle("Fusion")
        
        # 创建暗色调色板
        palette = QPalette()
        
        # 设置基本颜色
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        # 设置禁用状态颜色
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(127, 127, 127))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(127, 127, 127))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(127, 127, 127))
        
        # 应用调色板
        app.setPalette(palette)
        app.setStyleSheet("")  # 清除所有样式表
        
    @staticmethod
    def apply_win11_light_theme(app):
        """应用Windows 11风格的亮色主题"""
        app.setStyle("Fusion")
        app.setStyleSheet(WIN11_LIGHT_STYLE)
        
        # Windows 11风格将通过样式表而不是调色板实现
        # 但我们仍然使用一个基础调色板以防某些控件没有被样式表覆盖
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 103, 192))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 212))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(palette)
        
        # 应用窗口阴影和透明效果需要单独处理
        ThemeManager._apply_window_effects(app)
    
    @staticmethod
    def apply_win11_dark_theme(app):
        """应用Windows 11风格的暗色主题"""
        app.setStyle("Fusion")
        app.setStyleSheet(WIN11_DARK_STYLE)
        
        # 设置基础调色板
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(32, 32, 32))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(44, 44, 44))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(32, 32, 32))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 120, 212))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 212))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(palette)
        
        # 应用窗口阴影和透明效果需要单独处理
        ThemeManager._apply_window_effects(app)
    
    @staticmethod
    def _apply_window_effects(app):
        """应用Windows 11特有的窗口效果
        
        注意：这些效果大部分依赖于特定的Windows API，
        对于跨平台应用程序，我们需要在不同平台上采用不同的策略。
        """
        # 为所有顶级窗口安装事件过滤器来应用效果
        # 延迟执行，确保应用程序所有窗口都已创建
        QTimer.singleShot(100, lambda: ThemeManager._install_event_filters(app))
    
    @staticmethod
    def _install_event_filters(app):
        """为所有顶级窗口安装事件过滤器，以便应用特殊效果"""
        # 这里可以添加平台特定的代码
        # 比如在Windows上使用win32api来设置窗口样式
        # 在这里我们仅处理窗口圆角，因为其他效果需要平台特定API
        pass 