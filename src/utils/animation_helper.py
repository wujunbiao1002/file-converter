#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 动画辅助工具
版权所有 (c) 2025 Junly
"""

from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QComboBox, QSpinBox
from PyQt6.QtCore import QObject, QVariant
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush

def add_animation_properties(widget):
    """为控件添加动画所需的自定义属性
    
    Args:
        widget: 需要添加动画支持的Qt控件
    """
    # 检查是否已经添加了属性
    if widget.property("has_animation_props") is not None:
        return
    
    # 使用Qt的动态属性系统设置属性
    widget.setProperty("has_animation_props", True)
    widget.setProperty("hover_factor", 0.0)
    widget.setProperty("focus_factor", 0.0)
    
    # 保存原始的paintEvent方法
    original_paint_event = widget.paintEvent
    
    # 定义新的paintEvent方法，增加动画效果
    def enhanced_paint_event(self, event):
        # 调用原始的paintEvent方法
        original_paint_event(event)
        
        # 获取动画因子
        hover = self.property("hover_factor")
        focus = self.property("focus_factor")
        
        # 如果有动画因子，添加视觉效果
        if hover and hover > 0:
            # 添加鼠标悬停效果
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 计算悬停效果颜色
            if isinstance(self, QPushButton):
                # 按钮悬停效果
                if self.isDefault():
                    # 默认按钮使用主题色
                    color = QColor(0, 120, 212, int(40 * hover))
                else:
                    # 普通按钮使用灰色
                    color = QColor(0, 0, 0, int(20 * hover))
                
                # 绘制半透明覆盖层
                painter.fillRect(self.rect(), color)
            elif isinstance(self, (QLineEdit, QComboBox, QSpinBox)):
                # 输入框悬停效果 - 绘制边框
                pen = QPen(QColor(0, 120, 212, int(150 * hover)))
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 4, 4)
        
        if focus and focus > 0:
            # 添加焦点效果
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 绘制焦点边框
            if isinstance(self, (QLineEdit, QComboBox, QSpinBox, QPushButton)):
                pen = QPen(QColor(0, 120, 212, int(200 * focus)))
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 4, 4)
    
    # 替换paintEvent方法
    widget.paintEvent = lambda event: enhanced_paint_event(widget, event)

class AnimationHelper:
    """控件动画辅助类，用于管理所有控件的动画效果"""
    
    @staticmethod
    def setup_animation_for_widget(widget):
        """为单个控件设置动画支持
        
        Args:
            widget: 需要添加动画支持的Qt控件
        """
        if isinstance(widget, (QPushButton, QLineEdit, QComboBox, QSpinBox)):
            add_animation_properties(widget)
    
    @staticmethod
    def setup_animation_for_all(parent_widget):
        """为父控件及其所有子控件设置动画支持
        
        Args:
            parent_widget: 父控件
        """
        # 遍历所有子控件
        for widget in parent_widget.findChildren(QWidget):
            if isinstance(widget, (QPushButton, QLineEdit, QComboBox, QSpinBox)):
                add_animation_properties(widget)
        
        # 也为父控件添加属性
        if isinstance(parent_widget, (QPushButton, QLineEdit, QComboBox, QSpinBox)):
            add_animation_properties(parent_widget) 