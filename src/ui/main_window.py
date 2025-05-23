#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件转换工具 - 主窗口
版权所有 (c) 2025 Junly
"""

import os
import sys

# 将项目根目录添加到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QMessageBox, QFileDialog,
    QStatusBar, QProgressBar, QLabel, QWidget, QVBoxLayout,
    QApplication, QFrame, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt, QSize, QPoint, QRect, QRectF, QPropertyAnimation, QEasingCurve, QUrl
from PyQt6.QtGui import QAction, QIcon, QPainter, QColor, QPainterPath, QRegion, QPen, QDesktopServices, QCursor
from datetime import datetime

from ui.components.word_tab import WordTab
from ui.components.excel_tab import ExcelTab
from ui.components.markdown_tab import MarkdownTab
from ui.components.pdf_tab import PDFTab
from ui.components.image_tab import ImageTab
from ui.components.text_tab import TextTab
from ui.settings_window import SettingsWindow
from utils.theme_manager import ThemeManager
from utils.animation_helper import AnimationHelper
from utils.app_info import AppInfo

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, config):
        super().__init__()
        
        self.config = config
        self.init_ui()
        
        # 应用主题
        self.apply_theme()
        
        # 为所有控件添加动画支持
        AnimationHelper.setup_animation_for_all(self)
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口基本属性
        self.setWindowTitle(AppInfo.get_app_name())
        self.setMinimumSize(800, 600)
        
        # 如果启用了Windows 11风格，则设置无框窗口，但不设置透明背景
        theme = self.config.get("theme", "light")
        self.is_win11_style = theme.startswith("win11_")
        if self.is_win11_style:
            # 无框窗口
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            # 关闭半透明背景
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
            # 设置属性，减少重绘闪烁
            self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
            # 双缓冲绘制，减少闪烁
            self.setAttribute(Qt.WidgetAttribute.WA_PaintOnScreen, False)
            self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
            
            # 在初始化时设置圆角遮罩，避免每次重绘时重新计算
            # 延迟设置遮罩，确保窗口已完全创建
            QApplication.instance().processEvents()
            self._setup_rounded_mask()
            
            # 标记是否正在拖动，用于减少重绘
            self.is_dragging = False
        
        # 创建中央容器
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 如果是Windows 11风格，添加自定义标题栏
        if self.is_win11_style:
            self.title_bar = self.create_title_bar()
            self.main_layout.addWidget(self.title_bar)
        
        # 创建内容容器
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        
        if self.is_win11_style:
            # 使用圆角容器
            self.content_layout.setContentsMargins(10, 5, 10, 10)
        else:
            self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建菜单栏
        self.create_menus()
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.content_layout.addWidget(self.tabs)
        
        # 添加各功能标签页
        self.word_tab = WordTab(self.config)
        self.excel_tab = ExcelTab(self.config)
        self.markdown_tab = MarkdownTab(self.config)
        self.pdf_tab = PDFTab(self.config)
        self.image_tab = ImageTab(self.config)
        self.text_tab = TextTab(self.config)
        
        self.tabs.addTab(self.word_tab, "Word转换")
        self.tabs.addTab(self.excel_tab, "Excel转换")
        self.tabs.addTab(self.markdown_tab, "Markdown转换")
        self.tabs.addTab(self.pdf_tab, "PDF转换")
        self.tabs.addTab(self.image_tab, "图片处理")
        self.tabs.addTab(self.text_tab, "文本处理")
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.content_layout.addWidget(self.statusBar)
        
        # 添加进度条到状态栏
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.statusBar.addPermanentWidget(self.progress_bar)
        
        # 添加版权信息到状态栏右下角
        current_year = datetime.now().year
        
        # 添加版本号标签，使用AppInfo类获取版本信息
        version_label = QLabel(AppInfo.get_full_version())
        version_label.setStyleSheet("color: #888888; margin-right: 5px;")
        self.statusBar.addPermanentWidget(version_label)
        
        # 添加博客链接
        blog_link = QLabel('<a href="https://junly.top">访问Junly的博客</a>')
        blog_link.setStyleSheet("color: #0066cc; margin-right: 5px;")
        blog_link.setOpenExternalLinks(True)
        blog_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        blog_link.setToolTip("https://junly.top")
        self.statusBar.addPermanentWidget(blog_link)
        
        # 使用AppInfo类获取版权信息
        copyright_label = QLabel(AppInfo.get_copyright_text(current_year))
        copyright_label.setStyleSheet("color: #888888; margin-right: 5px;")
        self.statusBar.addPermanentWidget(copyright_label)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.statusBar.addWidget(self.status_label)
        
        # 添加内容容器到主布局
        self.main_layout.addWidget(self.content_container)
        
        # 设置拖放支持
        self.setAcceptDrops(True)
    
    def create_title_bar(self):
        """创建Windows 11风格的标题栏"""
        title_bar = QFrame()
        title_bar.setFixedHeight(32)
        title_bar.setCursor(Qt.CursorShape.ArrowCursor)  # 确保鼠标指针形状正确
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 0, 10, 0)
        title_bar_layout.setSpacing(0)
        
        # 添加应用图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icons", "app.png")
        icon_label = QLabel()
        if os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(16, 16))
        else:
            # 使用默认图标
            icon_label.setText("🔄")
        
        # 设置标签可拖动
        icon_label.mousePressEvent = self.title_bar_mouse_press
        title_bar_layout.addWidget(icon_label)
        title_bar_layout.addSpacing(8)
        
        # 添加标题文本
        title_label = QLabel(AppInfo.get_app_name())
        title_label.setStyleSheet("font-weight: bold;")
        # 设置标签可拖动
        title_label.mousePressEvent = self.title_bar_mouse_press
        title_label.mouseMoveEvent = self.title_bar_mouse_move
        title_label.mouseReleaseEvent = self.title_bar_mouse_release
        title_bar_layout.addWidget(title_label)
        
        # 添加可拖动的空白区域
        drag_area = QWidget()
        drag_area.setCursor(Qt.CursorShape.ArrowCursor)
        # 设置空白区域可拖动
        drag_area.mousePressEvent = self.title_bar_mouse_press
        drag_area.mouseMoveEvent = self.title_bar_mouse_move
        drag_area.mouseReleaseEvent = self.title_bar_mouse_release
        title_bar_layout.addWidget(drag_area, 1)  # 将空白区域设为可伸缩
        
        # 添加窗口控制按钮
        button_size = 28
        
        # 最小化按钮
        min_button = QPushButton("🗕")
        min_button.setFixedSize(button_size, button_size)
        min_button.clicked.connect(self.showMinimized)
        min_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        title_bar_layout.addWidget(min_button)
        
        # 最大化/还原按钮
        self.max_button = QPushButton("🗖")
        self.max_button.setFixedSize(button_size, button_size)
        self.max_button.clicked.connect(self.toggle_maximize)
        self.max_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        title_bar_layout.addWidget(self.max_button)
        
        # 关闭按钮
        close_button = QPushButton("✕")
        close_button.setFixedSize(button_size, button_size)
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
        """)
        title_bar_layout.addWidget(close_button)
        
        return title_bar
    
    def create_menus(self):
        """创建菜单栏"""
        # 文件菜单
        file_menu = self.menuBar().addMenu("文件")
        
        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = self.menuBar().addMenu("编辑")
        
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.open_settings)
        edit_menu.addAction(settings_action)
        
        # 更新菜单
        update_menu = self.menuBar().addMenu("更新")
        
        check_update_action = QAction("检查更新", self)
        check_update_action.triggered.connect(self.open_website)
        update_menu.addAction(check_update_action)
        
        # 帮助菜单
        help_menu = self.menuBar().addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        contact_action = QAction("联系方式", self)
        contact_action.triggered.connect(self.open_website)
        help_menu.addAction(contact_action)
    
    def open_file(self):
        """打开文件对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "", 
            "所有文件 (*);;Word文档 (*.docx *.doc);;Excel文档 (*.xlsx *.xls);;Markdown文档 (*.md);;PDF文档 (*.pdf);;图片文件 (*.jpg *.png *.bmp *.tiff);;文本文件 (*.txt)"
        )
        
        if file_path:
            self.process_file(file_path)
    
    def process_file(self, file_path):
        """处理打开的文件"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 根据文件扩展名切换到相应的标签页
        if file_ext in ['.doc', '.docx']:
            self.tabs.setCurrentWidget(self.word_tab)
            self.word_tab.set_input_file(file_path)
        elif file_ext in ['.xls', '.xlsx']:
            self.tabs.setCurrentWidget(self.excel_tab)
            self.excel_tab.set_input_file(file_path)
        elif file_ext == '.md':
            self.tabs.setCurrentWidget(self.markdown_tab)
            self.markdown_tab.set_input_file(file_path)
        elif file_ext == '.pdf':
            self.tabs.setCurrentWidget(self.pdf_tab)
            self.pdf_tab.set_input_file(file_path)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            self.tabs.setCurrentWidget(self.image_tab)
            self.image_tab.set_input_file(file_path)
        elif file_ext == '.txt':
            self.tabs.setCurrentWidget(self.text_tab)
            self.text_tab.set_input_file(file_path)
    
    def open_settings(self):
        """打开设置窗口"""
        # 记录旧的主题设置
        old_theme = self.config.get("theme")
        
        settings_dialog = SettingsWindow(self.config, self)
        if settings_dialog.exec():
            # 如果设置被接受，检查主题是否改变
            new_theme = self.config.get("theme")
            if old_theme != new_theme:
                # 检查主题变化是否涉及Windows 11风格切换
                if (old_theme.startswith("win11_") and not new_theme.startswith("win11_")) or \
                   (not old_theme.startswith("win11_") and new_theme.startswith("win11_")):
                    # 需要重启应用以应用窗口框架更改
                    QMessageBox.information(
                        self,
                        "需要重启",
                        "窗口样式变更需要重启应用才能完全生效。请手动重启应用。"
                    )
                else:
                    # 立即应用新主题
                    self.apply_theme()
                    
                    # 通知用户已应用新主题
                    QMessageBox.information(
                        self,
                        "主题已应用",
                        "新的主题设置已应用。"
                    )
        
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, 
            f"关于{AppInfo.get_app_name()}",
            AppInfo.get_about_text()
        )
    
    def dragEnterEvent(self, event):
        """拖入文件事件处理"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """放下文件事件处理"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.process_file(file_path)
    
    def update_status(self, message):
        """更新状态栏消息"""
        self.status_label.setText(message)
    
    def show_progress(self, value):
        """显示进度条"""
        if not self.progress_bar.isVisible():
            self.progress_bar.setVisible(True)
        
        self.progress_bar.setValue(value)
        
        if value >= 100:
            # 完成后隐藏进度条
            self.progress_bar.setVisible(False)
    
    def apply_theme(self):
        """应用当前主题"""
        theme = self.config.get("theme", "win11_light")
        
        # 创建淡入淡出动画效果
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(300)  # 300毫秒
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.7)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # 淡出
        self.fade_animation.start()
        
        # 连接动画完成信号
        self.fade_animation.finished.connect(self._apply_theme_and_fade_in)
    
    def _apply_theme_and_fade_in(self):
        """应用主题并淡入"""
        # 获取当前主题
        theme = self.config.get("theme", "win11_light")
        
        # 应用主题
        ThemeManager.apply_theme(QApplication.instance(), theme)
        
        # 强制刷新窗口和所有子控件
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        
        # 刷新所有子控件
        for child in self.findChildren(QWidget):
            child.style().unpolish(child)
            child.style().polish(child)
            child.update()
        
        # 创建淡入动画
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(300)  # 300毫秒
        self.fade_in_animation.setStartValue(0.7)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in_animation.start()
    
    def _setup_rounded_mask(self):
        """设置圆角窗口遮罩"""
        if not hasattr(self, "is_win11_style") or not self.is_win11_style:
            return
        
        try:    
            # 创建圆角矩形路径
            rect = self.rect()
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 10, 10)
            
            # 创建圆角区域
            region = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(region)
        except Exception as e:
            print(f"设置窗口遮罩出错: {e}")
    
    def resizeEvent(self, event):
        """窗口大小改变事件，更新圆角遮罩"""
        super().resizeEvent(event)
        if hasattr(self, "is_win11_style") and self.is_win11_style:
            self._setup_rounded_mask()
    
    def paintEvent(self, event):
        """绘制事件，用于实现圆角窗口和阴影效果"""
        theme = self.config.get("theme", "light")
        
        if theme.startswith("win11_"):
            # 拖动过程中使用最简单的绘制方式
            if hasattr(self, "is_dragging") and self.is_dragging:
                painter = QPainter(self)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
                
                # 简单背景填充
                if theme == "win11_light":
                    painter.fillRect(self.rect(), QColor(245, 245, 245))
                else:
                    painter.fillRect(self.rect(), QColor(32, 32, 32))
                return
            
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 禁用背景自动填充
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
            
            # 创建圆角矩形路径
            rect = self.rect()
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect), 10, 10)
            
            # 检查是否正在拖动中
            is_dragging = self.property("no_shadows_during_drag")
            
            # 绘制不透明背景 - 移除透明度
            if theme == "win11_light":
                # 浅色主题背景 - 完全不透明
                bg_color = QColor(245, 245, 245)
                painter.fillPath(path, bg_color)
                
                # 仅在非拖动状态添加更多细节
                if not is_dragging:
                    # 为浅色主题添加一点点边框以增加层次感
                    pen = QPen(QColor(200, 200, 200))
                    pen.setWidth(1)
                    painter.setPen(pen)
                    painter.drawPath(path)
            else:
                # 暗色主题背景 - 完全不透明
                bg_color = QColor(32, 32, 32)
                painter.fillPath(path, bg_color)
                
                # 仅在非拖动状态添加更多细节
                if not is_dragging:
                    # 为暗色主题添加一点点亮边框增加层次感
                    pen = QPen(QColor(70, 70, 70))
                    pen.setWidth(1)
                    painter.setPen(pen)
                    painter.drawPath(path)
            
            # 不再每次都重新设置遮罩，提高性能
            # 遮罩设置移到_setup_rounded_mask和resizeEvent中处理
    
    # 标题栏鼠标事件处理（专门用于标题栏控件）
    def title_bar_mouse_press(self, event):
        """标题栏鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 保存鼠标全局位置，避免坐标转换引起的误差
            self._drag_pos = event.globalPosition()
            self._window_pos = self.mapToGlobal(QPoint(0, 0))
            
            if hasattr(self, "is_win11_style") and self.is_win11_style:
                # 标记开始拖动
                self.is_dragging = True
                # 设置拖动标志，降低绘制复杂度
                self.setProperty("no_shadows_during_drag", True)
                # 最小化更新区域
                self.update(QRect(0, 0, self.width(), 1))
            event.accept()
    
    def title_bar_mouse_move(self, event):
        """标题栏鼠标移动事件"""
        if hasattr(self, '_drag_pos') and self.is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # 使用全局坐标直接计算偏移，避免坐标空间转换
            current_global_pos = event.globalPosition()
            delta = current_global_pos - self._drag_pos
            
            # 计算新位置
            new_x = int(self._window_pos.x() + delta.x())
            new_y = int(self._window_pos.y() + delta.y())
            
            # 直接使用整数坐标移动窗口，避免浮点误差
            self.move(new_x, new_y)
            event.accept()
    
    def title_bar_mouse_release(self, event):
        """标题栏鼠标释放事件"""
        if hasattr(self, '_drag_pos'):
            del self._drag_pos
            if hasattr(self, "is_win11_style") and self.is_win11_style:
                # 标记结束拖动
                self.is_dragging = False
                # 恢复阴影效果
                self.setProperty("no_shadows_during_drag", False)
                self.update()
            event.accept()
            
    def mousePressEvent(self, event):
        """鼠标按下事件，用于实现窗口拖动"""
        # 无论是什么主题，都保存鼠标点击位置
        if event.button() == Qt.MouseButton.LeftButton:
            # 保存鼠标全局位置和窗口位置
            self._drag_pos = event.globalPosition()
            self._window_pos = self.mapToGlobal(QPoint(0, 0))
            
            # 标记开始拖动
            self.is_dragging = True
            # 取消阴影动画效果，提高拖动性能
            if hasattr(self, "is_win11_style") and self.is_win11_style:
                self.setProperty("no_shadows_during_drag", True)
                # 最小化更新区域
                self.update(QRect(0, 0, self.width(), 1))
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，用于实现窗口拖动"""
        # 确保任何主题下都能拖动窗口
        if hasattr(self, '_drag_pos') and self.is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # 使用全局坐标直接计算偏移，避免坐标空间转换
            current_global_pos = event.globalPosition()
            delta = current_global_pos - self._drag_pos
            
            # 计算新位置，使用整数坐标
            new_x = int(self._window_pos.x() + delta.x())
            new_y = int(self._window_pos.y() + delta.y())
            
            # 使用move而不是setGeometry来避免不必要的布局重计算
            self.move(new_x, new_y)
            event.accept()
            return
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，结束窗口拖动"""
        if hasattr(self, '_drag_pos'):
            del self._drag_pos
            # 标记结束拖动
            self.is_dragging = False
            # 恢复阴影效果
            if hasattr(self, "is_win11_style") and self.is_win11_style:
                self.setProperty("no_shadows_during_drag", False)
                self.update()
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def toggle_maximize(self):
        """切换窗口最大化/还原状态"""
        if self.isMaximized():
            self.showNormal()
            self.max_button.setText("🗖")
        else:
            self.showMaximized()
            self.max_button.setText("🗗")
    
    def open_website(self):
        """打开网站"""
        QDesktopServices.openUrl(QUrl("https://junly.top/posts/soft-file-converter")) 