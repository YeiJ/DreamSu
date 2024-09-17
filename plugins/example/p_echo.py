# plugins\example\p_echo.py
# __version__ = "1.0.0"

from plugin_base import Plugin
import logging
from api.send import send_msg

logger = logging.getLogger("bot")

class P_echoPlugin(Plugin):
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        user_id = message['user_id']
        raw_message = message['raw_message']
        message_type = message.get('message_type', '')  # 获取消息类型，默认为空字符串
        # logger.info("Echo 插件接收到了该消息", message)  # 添加日志输出以确认消息接收

        # 仅复读私聊消息
        if message_type == 'private':  # 这里的 'private' 需要根据实际消息类型值来调整

            # 复读消息
            send_msg(self.bot.base_url, "private", user_id, raw_message, self.bot.token)
            logger.info("Echo 插件成功复读消息\n")
        else:
            #logger.info("Echo 插件忽略群组消息\n", message)
            pass 
