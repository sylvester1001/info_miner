import json
import os
import logging
from datetime import datetime

class HistoryManager:
    def __init__(self, history_file='data/history.json'):
        self.history_file = history_file
        self.history = self._load_history()
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger(__name__)

    def _load_history(self):
        """加载历史记录文件"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                return {}
        else:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            return {}

    def _save_history(self):
        """保存历史记录到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving history: {str(e)}")

    def is_url_seen(self, keyword, url):
        """检查URL是否已经在历史记录中"""
        if keyword not in self.history:
            self.history[keyword] = {'urls': []}
        return url in self.history[keyword]['urls']

    def add_result(self, keyword, result):
        """添加新的搜索结果到历史记录"""
        if keyword not in self.history:
            self.history[keyword] = {'urls': []}
        
        if result['url'] not in self.history[keyword]['urls']:
            self.history[keyword]['urls'].append(result['url'])
            self._save_history()

    def get_history_for_keyword(self, keyword):
        """获取某个关键词的所有历史记录"""
        return self.history.get(keyword, {'urls': []})

    def clear_history(self, keyword=None):
        """清除历史记录
        如果指定了keyword，只清除该关键词的历史
        否则清除所有历史
        """
        if keyword:
            if keyword in self.history:
                del self.history[keyword]
        else:
            self.history = {}
        self._save_history() 