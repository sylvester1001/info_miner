import os
import json
from datetime import datetime
import logging

class Utils:
    @staticmethod
    def ensure_directory(directory):
        """确保目录存在，如果不存在则创建"""
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

    @staticmethod
    def get_today_str():
        """获取今天的日期字符串"""
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def load_json(file_path):
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading JSON file {file_path}: {str(e)}")
            return None

    @staticmethod
    def save_json(data, file_path):
        """保存数据到JSON文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"Data saved to {file_path}")
            return True
        except Exception as e:
            logging.error(f"Error saving JSON file {file_path}: {str(e)}")
            return False

    @staticmethod
    def sanitize_filename(filename):
        """清理文件名，移除不合法字符"""
        return "".join([c for c in filename if c.isalnum() or c in (' ', '-', '_')]).rstrip() 