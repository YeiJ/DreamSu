# log.py

import logging
from datetime import datetime
import os
import json
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

def async_log_write(func):
    """包装函数，使其异步执行"""
    def wrapper(*args, **kwargs):
        return executor.submit(func, *args, **kwargs)
    return wrapper

@async_log_write
def write_log_async(logger, message, level):
    """异步写入日志"""
    if level == 'INFO':
        logger.info(message)
    elif level == 'ERROR':
        logger.error(message)
    elif level == 'WARNING':
        logger.warning(message)
    else:
        logger.debug(message)

def setup_logging():
    """设置日志记录"""

    # 读取配置文件中的日志级别
    config_path = "config/config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    log_level_str = config.get("log_level", "info").upper()  # 从配置文件读取日志级别并转为大写
    log_level = getattr(logging, log_level_str, logging.INFO)  # 获取日志级别的数值，如果无效默认INFO

    log_dir = "logs"

    # 创建日志文件的目录（如果不存在）
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 设置文件后缀
    suffix = ".log"

    # 重命名已有的 latest.log 文件
    latest_log_path = os.path.join(log_dir, f"latest{suffix}")
    if os.path.exists(latest_log_path):
        # 获取文件修改日期并格式化
        modification_time = os.path.getmtime(latest_log_path)
        modification_date = datetime.fromtimestamp(modification_time).strftime('%Y%m%d_%H%M%S')
        old_log_filename = os.path.join(log_dir, f"{modification_date}{suffix}")
        
        # 检查是否存在同名文件并重命名
        counter = 1
        while os.path.exists(old_log_filename):
            # 追加计数器到文件名以避免命名冲突
            old_log_filename = os.path.join(log_dir, f"{modification_date}_{counter}{suffix}")
            counter += 1
        
        os.rename(latest_log_path, old_log_filename)

    # 设置新的最新日志文件路径
    log_filename = latest_log_path

    # 检查并删除多余的日志文件，保留最新的15个
    manage_log_files(log_dir, suffix, keep_count=15)

    # 清空默认的 root logger 中的 handlers，避免重复日志
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # 创建一个 FileHandler 以确保日志使用 utf-8 编码
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    # 配置 root logger
    logging.getLogger().setLevel(log_level)  # 使用配置文件中的日志级别
    logging.getLogger().addHandler(file_handler)
    
    # 创建一个 StreamHandler 来同时在控制台输出日志
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)  # 使用配置文件中的日志级别
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    # 确保日志立即写入文件
    file_handler.flush()
    # 将 StreamHandler 添加到 root logger
    logging.getLogger().addHandler(console_handler)

def manage_log_files(directory, suffix, keep_count=30):
    """管理日志文件，确保目录中保留最新的 keep_count 个日志文件"""
    # 仅获取带有指定后缀的日志文件
    log_files = [f for f in os.listdir(directory) if f.endswith(suffix) and os.path.isfile(os.path.join(directory, f))]

    # 按照文件的修改时间排序
    log_files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)

    # 删除超过保留数量的日志文件
    for log_file in log_files[keep_count:]:
        os.remove(os.path.join(directory, log_file))

# 在调用时异步写入日志：
logger = logging.getLogger(__name__)
write_log_async(logger, "这是一个异步日志消息喵～", "INFO")
