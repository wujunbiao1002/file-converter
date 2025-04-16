#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 日志记录工具
版权所有 (c) 2025 Junly
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import datetime
import sys

# 全局日志对象
logger = None

def setup_logger():
    """设置日志记录器"""
    global logger
    if logger is not None:
        return logger
    
    # 创建日志目录
    log_dir = Path.home() / ".file-converter" / "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # 日志文件路径
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"file-converter-{today}.log"
    
    # 创建日志记录器
    logger = logging.getLogger("file-converter")
    logger.setLevel(logging.DEBUG)
    
    # 文件处理器 - 使用循环日志文件
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 日志格式
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("日志系统初始化完成")
    
    return logger

def get_logger():
    """获取日志对象"""
    global logger
    if logger is None:
        logger = setup_logger()
    return logger

# 便捷日志函数
def debug(message):
    """记录调试级别日志"""
    get_logger().debug(message)

def info(message):
    """记录信息级别日志"""
    get_logger().info(message)

def warning(message):
    """记录警告级别日志"""
    get_logger().warning(message)

def error(message):
    """记录错误级别日志"""
    get_logger().error(message)

def critical(message):
    """记录严重级别日志"""
    get_logger().critical(message)

def exception(message):
    """记录异常信息，包含堆栈跟踪"""
    get_logger().exception(message) 