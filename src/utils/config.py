#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Junly文件转换工具 - 配置管理工具
版权所有 (c) 2025 Junly
"""

import os
import json
from pathlib import Path

class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config_path = self._get_config_path()
        
        # 默认配置
        self.defaults = {
            "default_output_path": str(Path.home() / "Downloads"),
            "language": "zh_CN",
            "theme": "win11_light",
            "recent_files": [],
            "max_recent_files": 10,
            "batch_threads": 4
        }
        
        # 当前配置，初始化为默认值
        self.settings = self.defaults.copy()
    
    def _get_config_path(self):
        """获取配置文件路径"""
        # 在用户主目录下创建配置目录
        app_dir = Path.home() / ".file-converter"
        os.makedirs(app_dir, exist_ok=True)
        
        return app_dir / "config.json"
    
    def load(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    
                    # 更新配置，保留默认值
                    for key, value in loaded_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
        except Exception as e:
            print(f"加载配置失败: {str(e)}")
            # 配置加载失败时使用默认配置
            self.settings = self.defaults.copy()
    
    def save(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置失败: {str(e)}")
            return False
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.settings.get(key, default if default is not None else self.defaults.get(key))
    
    def set(self, key, value):
        """设置配置项"""
        if key in self.settings:
            self.settings[key] = value
        
    def add_recent_file(self, file_path):
        """添加最近使用的文件"""
        recent_files = self.get("recent_files", [])
        
        # 如果文件已在列表中，先移除它
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # 将文件添加到列表最前面
        recent_files.insert(0, file_path)
        
        # 保持列表长度不超过最大限制
        max_files = self.get("max_recent_files")
        if len(recent_files) > max_files:
            recent_files = recent_files[:max_files]
        
        # 更新配置
        self.set("recent_files", recent_files)
        
        # 保存配置
        self.save()
    
    def clear_recent_files(self):
        """清空最近使用的文件列表"""
        self.set("recent_files", [])
        self.save()
    
    def get_recent_files(self):
        """获取最近使用的文件列表"""
        return self.get("recent_files", []) 