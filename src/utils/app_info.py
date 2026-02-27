#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件转换工具 - 应用信息管理
版权所有 (c) 2025 Junly
"""

from datetime import datetime


class AppInfo:
    """应用信息类，用于集中管理应用信息"""

    # 应用名称
    NAME = "Junly文件转换工具"

    # 应用版本号
    VERSION = "1.0.4"

    # 版本号前缀
    VERSION_PREFIX = "v"

    # 完整版本号（前缀 + 版本号）
    FULL_VERSION = f"{VERSION_PREFIX}{VERSION}"

    # 应用作者
    AUTHOR = "Junly"

    # 应用版权年份起始
    COPYRIGHT_YEAR_START = "2025"

    @classmethod
    def get_version(cls):
        """获取版本号"""
        return cls.VERSION

    @classmethod
    def get_full_version(cls):
        """获取完整版本号（带前缀）"""
        return cls.FULL_VERSION

    @classmethod
    def get_copyright_text(cls, current_year=None):
        """获取版权文本

        Args:
            current_year: 当前年份，如果为None则自动获取

        Returns:
            str: 格式化的版权文本
        """
        if current_year is None:
            current_year = datetime.now().year

        copyright_year = (
            f"{cls.COPYRIGHT_YEAR_START}-{current_year}"
            if int(current_year) > int(cls.COPYRIGHT_YEAR_START)
            else cls.COPYRIGHT_YEAR_START
        )
        return f"@{copyright_year} {cls.AUTHOR}"

    @classmethod
    def get_app_name(cls):
        """获取应用名称"""
        return cls.NAME

    @classmethod
    def get_about_text(cls, copyright_year=None):
        """获取关于文本"""
        if not copyright_year:
            current_year = datetime.now().year
            copyright_year = (
                f"{cls.COPYRIGHT_YEAR_START}-{current_year}"
                if int(current_year) > int(cls.COPYRIGHT_YEAR_START)
                else cls.COPYRIGHT_YEAR_START
            )
        return (
            f"{cls.NAME} {cls.FULL_VERSION}\n\n"
            f"一个用于各种文件格式转换的工具\n\n"
            f"联系方式: https://junly.top\n"
            f"@{copyright_year} By {cls.AUTHOR}"
        )
