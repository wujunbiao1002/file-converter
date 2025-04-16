#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件转换器 - 图片处理核心模块
版权所有 (c) 2025 Junly
"""

import os
import shutil
from PIL import Image
from pathlib import Path

class ImageProcessor:
    """图片处理类"""
    
    def __init__(self):
        """初始化图片处理器"""
        # 支持的图片格式
        self.supported_formats = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'bmp': 'BMP',
            'tiff': 'TIFF',
            'webp': 'WEBP',
            'gif': 'GIF'
        }
    
    def convert_format(self, input_path, output_path, target_format, progress_callback=None):
        """转换图片格式"""
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 获取Pillow支持的格式名称
            if target_format.lower() not in self.supported_formats:
                raise Exception(f"不支持的图片格式: {target_format}")
            
            pil_format = self.supported_formats[target_format.lower()]
            
            # 打开并转换图片
            with Image.open(input_path) as img:
                # 转换格式
                if pil_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                    # JPEG不支持透明通道，转换为RGB
                    img = img.convert('RGB')
                
                # 保存为目标格式
                img.save(output_path, format=pil_format)
            
            # 更新进度
            if progress_callback:
                progress_callback(100)
            
            return True
            
        except Exception as e:
            raise Exception(f"格式转换失败: {str(e)}")
    
    def batch_convert_format(self, input_files, output_dir, target_format, progress_callback=None):
        """批量转换图片格式"""
        try:
            results = []
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 处理所有图片
            for i, input_path in enumerate(input_files):
                try:
                    # 生成输出文件路径
                    filename = os.path.basename(input_path)
                    name_without_ext = os.path.splitext(filename)[0]
                    output_path = os.path.join(output_dir, f"{name_without_ext}.{target_format.lower()}")
                    
                    # 转换格式
                    self.convert_format(input_path, output_path, target_format)
                    
                    results.append((input_path, output_path, True, ""))
                except Exception as e:
                    results.append((input_path, "", False, str(e)))
                
                # 更新进度
                if progress_callback:
                    progress_callback(int((i+1) / len(input_files) * 100))
            
            return results
            
        except Exception as e:
            raise Exception(f"批量格式转换失败: {str(e)}")
    
    def resize_image(self, input_path, output_path, width, height, keep_aspect_ratio=True, progress_callback=None):
        """调整图片尺寸"""
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 打开图片
            with Image.open(input_path) as img:
                # 如果保持纵横比，计算新尺寸
                if keep_aspect_ratio:
                    original_width, original_height = img.size
                    aspect_ratio = original_width / original_height
                    
                    if width == 0:
                        # 根据高度计算宽度
                        width = int(height * aspect_ratio)
                    elif height == 0:
                        # 根据宽度计算高度
                        height = int(width / aspect_ratio)
                    else:
                        # 按照宽高比较小的一边缩放
                        width_ratio = width / original_width
                        height_ratio = height / original_height
                        
                        if width_ratio < height_ratio:
                            height = int(width / aspect_ratio)
                        else:
                            width = int(height * aspect_ratio)
                
                # 调整尺寸
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # 保存图片
                resized_img.save(output_path)
            
            # 更新进度
            if progress_callback:
                progress_callback(100)
            
            return True
            
        except Exception as e:
            raise Exception(f"调整尺寸失败: {str(e)}")
    
    def batch_resize_image(self, input_files, output_dir, width, height, keep_aspect_ratio=True, progress_callback=None):
        """批量调整图片尺寸"""
        try:
            results = []
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 处理所有图片
            for i, input_path in enumerate(input_files):
                try:
                    # 生成输出文件路径
                    filename = os.path.basename(input_path)
                    output_path = os.path.join(output_dir, filename)
                    
                    # 调整尺寸
                    self.resize_image(input_path, output_path, width, height, keep_aspect_ratio)
                    
                    results.append((input_path, output_path, True, ""))
                except Exception as e:
                    results.append((input_path, "", False, str(e)))
                
                # 更新进度
                if progress_callback:
                    progress_callback(int((i+1) / len(input_files) * 100))
            
            return results
            
        except Exception as e:
            raise Exception(f"批量调整尺寸失败: {str(e)}")
    
    def compress_image(self, input_path, output_path, quality=85, progress_callback=None):
        """压缩图片"""
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 打开图片
            with Image.open(input_path) as img:
                # 获取原始格式
                original_format = img.format
                
                # 转换模式以适应JPEG格式
                if original_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')
                
                # 保存时使用较低的质量参数
                if original_format == 'JPEG':
                    img.save(output_path, quality=quality, optimize=True)
                elif original_format == 'PNG':
                    # PNG使用不同的优化方法
                    img.save(output_path, format='PNG', optimize=True, compress_level=9)
                else:
                    # 其他格式
                    img.save(output_path)
            
            # 更新进度
            if progress_callback:
                progress_callback(100)
            
            # 返回压缩前后的文件大小
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            return original_size, compressed_size
            
        except Exception as e:
            raise Exception(f"压缩图片失败: {str(e)}")
    
    def batch_compress_image(self, input_files, output_dir, quality=85, progress_callback=None):
        """批量压缩图片"""
        try:
            results = []
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 处理所有图片
            for i, input_path in enumerate(input_files):
                try:
                    # 生成输出文件路径
                    filename = os.path.basename(input_path)
                    output_path = os.path.join(output_dir, filename)
                    
                    # 压缩图片
                    original_size, compressed_size = self.compress_image(input_path, output_path, quality)
                    
                    # 计算压缩率
                    compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
                    
                    results.append((input_path, output_path, True, f"压缩率: {compression_ratio:.2f}%"))
                except Exception as e:
                    results.append((input_path, "", False, str(e)))
                
                # 更新进度
                if progress_callback:
                    progress_callback(int((i+1) / len(input_files) * 100))
            
            return results
            
        except Exception as e:
            raise Exception(f"批量压缩图片失败: {str(e)}")
    
    def get_image_info(self, image_path):
        """获取图片信息"""
        try:
            with Image.open(image_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'file_size': os.path.getsize(image_path) / 1024,  # KB
                }
        except Exception as e:
            raise Exception(f"获取图片信息失败: {str(e)}") 