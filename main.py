# main.py

from bot import Bot
from log import setup_logging  # 导入 setup_logging 函数
    
if __name__ == "__main__":
    # 设置日志记录
    setup_logging()
    
    # 初始化 Bot 实例并启动
    bot = Bot()
    bot.start()
