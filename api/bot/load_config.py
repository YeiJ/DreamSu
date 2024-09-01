# bot/api/load_config.py

import json
import logging

def load_config(self, file_path, encoding=None):
    """从 JSON 文件中加载配置"""
    try:
        if encoding:
            with open(file_path, 'r', encoding=encoding) as file:
                config = json.load(file)
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
        return config
    except FileNotFoundError:
        logging.error(f"错误：文件 {file_path} 未找到")
        return {}
    except json.JSONDecodeError:
        logging.error(f"错误：文件 {file_path} 的 JSON 解析失败")
        return {}
    except Exception as e:
        logging.error(f"错误：读取文件 {file_path} 时出现异常: {e}")
        return {}
