#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件转换工具 - 主题管理工具
版权所有 (c) 2025 Junly
"""

from PyQt6.QtWidgets import QApplication, QPushButton, QLineEdit, QAbstractButton, QCheckBox, QRadioButton, QComboBox, QListView, QListWidget
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QEvent, QTimer, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QObject, Qt
from ui.themes.win11_theme import WIN11_LIGHT_STYLE, WIN11_DARK_STYLE
from utils.animation_helper import AnimationHelper
import sys
import ctypes

class WidgetAnimationFilter(QObject):
    """控件动画效果过滤器"""
    
    def __init__(self, parent):
        super().__init__(parent)
        # 存储控件动画
        self.hover_animations = {}
        self.focus_animations = {}
    
    def eventFilter(self, obj, event):
        # 处理按钮悬停事件
        if isinstance(obj, QAbstractButton) and not isinstance(obj, QCheckBox) and not isinstance(obj, QRadioButton):
            # 确保控件有动画属性
            AnimationHelper.setup_animation_for_widget(obj)
            
            if event.type() == QEvent.Type.Enter:
                self._start_hover_animation(obj, True)
                return False
            elif event.type() == QEvent.Type.Leave:
                self._start_hover_animation(obj, False)
                return False
        
        # 处理输入框焦点事件
        if isinstance(obj, QLineEdit) or isinstance(obj, QComboBox):
            # 确保控件有动画属性
            AnimationHelper.setup_animation_for_widget(obj)
            
            if event.type() == QEvent.Type.FocusIn:
                self._start_focus_animation(obj, True)
                return False
            elif event.type() == QEvent.Type.FocusOut:
                self._start_focus_animation(obj, False)
                return False
        
        return super().eventFilter(obj, event)
    
    def _start_hover_animation(self, widget, hover_in):
        """开始悬停动画效果"""
        if widget in self.hover_animations:
            self.hover_animations[widget].stop()
        
        # 创建动画
        animation = QPropertyAnimation(widget, b"hover_factor")
        animation.setDuration(150)  # 150毫秒
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if hover_in:
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
        else:
            animation.setStartValue(widget.property("hover_factor") or 0.0)
            animation.setEndValue(0.0)
        
        # 连接值变化信号
        animation.valueChanged.connect(lambda value: self._update_hover_style(widget, value))
        
        # 保存并启动动画
        self.hover_animations[widget] = animation
        animation.start()
    
    def _update_hover_style(self, widget, value):
        """更新控件悬停样式"""
        # 设置新的属性值
        widget.setProperty("hover_factor", value)
        # 强制重绘
        widget.update()
    
    def _start_focus_animation(self, widget, focus_in):
        """开始焦点动画效果"""
        if widget in self.focus_animations:
            self.focus_animations[widget].stop()
        
        # 创建动画
        animation = QPropertyAnimation(widget, b"focus_factor")
        animation.setDuration(200)  # 200毫秒
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if focus_in:
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
        else:
            animation.setStartValue(widget.property("focus_factor") or 0.0)
            animation.setEndValue(0.0)
        
        # 连接值变化信号
        animation.valueChanged.connect(lambda value: self._update_focus_style(widget, value))
        
        # 保存并启动动画
        self.focus_animations[widget] = animation
        animation.start()
    
    def _update_focus_style(self, widget, value):
        """更新控件焦点样式"""
        # 设置新的属性值
        widget.setProperty("focus_factor", value)
        # 强制重绘
        widget.update()

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
        
        # 自定义控件样式，确保颜色正确
        ThemeManager._fix_custom_styles(app, is_dark=False)
        
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
        
        # 自定义控件样式，确保颜色正确
        ThemeManager._fix_custom_styles(app, is_dark=True)
        
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
        # 安装全局事件过滤器用于控件动画效果
        app.installEventFilter(WidgetAnimationFilter(app))
        
        # 尝试导入Windows特定API (仅在Windows平台上)
        try:
            if sys.platform == 'win32':
                # 检查是否有pywin32模块
                import win32gui
                import win32con
                import win32api
                
                # 获取所有顶级窗口
                top_windows = app.topLevelWidgets()
                for window in top_windows:
                    # 获取窗口句柄
                    hwnd = int(window.winId())
                    if hwnd and win32gui.IsWindow(hwnd):
                        # Windows 11/10 上使用DWM扩展窗口框架实现圆角和阴影
                        try:
                            # 尝试导入dwmapi模块 (需要pywin32扩展)
                            import comtypes.client as cc
                            
                            # 创建DwmEnableBlurBehindWindow函数需要的结构体
                            class DWM_BLURBEHIND(ctypes.Structure):
                                _fields_ = [
                                    ('dwFlags', ctypes.c_uint),
                                    ('fEnable', ctypes.c_bool),
                                    ('hRgnBlur', ctypes.c_void_p),
                                    ('fTransitionOnMaximized', ctypes.c_bool)
                                ]
                            
                            # 创建Windows 11圆角效果
                            DWMWCP_DEFAULT = 0
                            DWMWCP_DONOTROUND = 1
                            DWMWCP_ROUND = 2
                            DWMWCP_ROUNDSMALL = 3
                            
                            # Windows 11 DWM属性
                            DWMWA_WINDOW_CORNER_PREFERENCE = 33  # Windows 11中的圆角首选项
                            
                            # 获取dwmapi
                            dwmapi = cc.GetModule("dwmapi.dll")
                            DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute
                            
                            # 设置圆角属性
                            DwmSetWindowAttribute(
                                hwnd,
                                DWMWA_WINDOW_CORNER_PREFERENCE, 
                                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                                ctypes.sizeof(ctypes.c_int)
                            )
                            
                            # 启用窗口阴影
                            win32gui.SetClassLong(
                                hwnd,
                                win32con.GCL_STYLE,
                                win32gui.GetClassLong(hwnd, win32con.GCL_STYLE) | win32con.CS_DROPSHADOW
                            )
                        except (ImportError, AttributeError, TypeError, Exception) as e:
                            # 如果DWM扩展不可用，回退到基本的Qt实现
                            pass
        except (ImportError, AttributeError):
            # 如果win32gui不可用，使用Qt的基本实现
            pass 
    
    @staticmethod
    def _fix_custom_styles(app, is_dark):
        """修复自定义控件样式，确保颜色显示正确
        
        Args:
            app: QApplication实例
            is_dark: 是否为深色主题
        """
        # 为所有现有的ComboBox设置正确的样式
        for widget in app.allWidgets():
            # 修复ComboBox下拉列表的文字颜色
            if isinstance(widget, QComboBox):
                # 获取下拉列表视图
                view = widget.view()
                if isinstance(view, QListView):
                    # 设置文字颜色
                    if is_dark:
                        view.setStyleSheet("QAbstractItemView { color: #ffffff; background-color: #2c2c2c; }")
                    else:
                        view.setStyleSheet("QAbstractItemView { color: #000000; background-color: #ffffff; }")
            
            # 修复QListWidget项的前景色问题
            if isinstance(widget, QListWidget):
                # 设置基本样式
                if is_dark:
                    widget.setStyleSheet("""
                        QListWidget {
                            background-color: #2c2c2c;
                            border: 1px solid #3a3a3a;
                            border-radius: 4px;
                        }
                        QListWidget::item {
                            color: #ffffff;
                            padding: 4px 8px;
                            margin: 2px;
                            border-radius: 4px;
                        }
                        QListWidget::item:selected {
                            background-color: #2c5c94;
                            border: 1px solid #0078d4;
                            color: #ffffff;
                        }
                        QListWidget::item:hover:!selected {
                            background-color: #3a3a3a;
                            border: 1px solid #505050;
                        }
                    """)
                else:
                    widget.setStyleSheet("""
                        QListWidget {
                            background-color: #ffffff;
                            border: 1px solid #e0e0e0;
                            border-radius: 4px;
                        }
                        QListWidget::item {
                            color: #000000;
                            padding: 4px 8px;
                            margin: 2px;
                            border-radius: 4px;
                        }
                        QListWidget::item:selected {
                            background-color: #e5f1fb;
                            border: 1px solid #0067c0;
                            color: #000000;
                        }
                        QListWidget::item:hover:!selected {
                            background-color: #f0f0f0;
                            border: 1px solid #e0e0e0;
                        }
                    """)
                
                # 确保QListWidget项的自定义前景色得到保留
                for i in range(widget.count()):
                    item = widget.item(i)
                    # 保存当前项的前景色
                    brush = item.foreground()
                    # 如果项有自定义前景色(不是默认色)，确保它被保留
                    if brush != widget.palette().text():
                        # 重新应用前景色以确保其优先级
                        color = brush.color()
                        # 使用setData而不是setForeground以确保兼容性
                        item.setData(Qt.ItemDataRole.ForegroundRole, color)
                
                # 强制刷新视图确保显示正确
                widget.repaint() 