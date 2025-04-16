#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 主程序入口
版权所有 (c) 2025 Junly
"""

import sys
import os
import signal
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from ui.main_window import MainWindow
from utils.logger import setup_logger, get_logger
from utils.config import Config
from utils.theme_manager import ThemeManager

def main():
    """主程序入口函数"""
    # 设置日志
    setup_logger()
    logger = get_logger()
    
    # 加载配置
    config = Config()
    config.load()
    
    # 创建Qt应用
    app = QApplication(sys.argv)
    app.setApplicationName("文件转换器")
    
    # 应用主题
    theme = config.get("theme", "light")
    ThemeManager.apply_theme(app, theme)
    
    # 设置应用图标
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "app.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # 创建主窗口
    window = MainWindow(config)
    window.show()
    
    # 设置信号处理，确保应用程序可以被正常终止
    def signal_handler(sig, frame):
        logger.info(f"接收到信号 {sig}，准备退出")
        # 延迟退出以确保所有资源正确清理
        QTimer.singleShot(0, app.quit)
        
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 确保Python解释器每隔一段时间处理信号
    timer = QTimer()
    timer.start(500)  # 每500毫秒
    timer.timeout.connect(lambda: None)  # 保持解释器活动以处理信号
    
    # 确保所有线程在应用退出时都能正确关闭
    app.aboutToQuit.connect(lambda: logger.info("应用程序即将退出，清理资源"))
    
    # 运行应用
    exit_code = app.exec()
    
    # 应用程序结束，确保所有资源释放
    logger.info("应用程序已退出")
    return exit_code

if __name__ == "__main__":
    sys.exit(main()) 