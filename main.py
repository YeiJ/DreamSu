# main.py

from bot import Bot
from log import setup_logging, logger 
    
if __name__ == "__main__":
    # 设置日志记录
    setup_logging()
    
    # 初始化 Bot 实例并启动
    bot = Bot()

    try:
        bot.start()
    except KeyboardInterrupt:
        logger.info("收到退出信号，正在优雅地关闭程序...")
    finally:
        logger.info("DreamSu框架已停止。")
