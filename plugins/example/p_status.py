# plugins/example/p_status.py
# __version__ = "1.0.1"

from plugin_base import Plugin
import logging
import psutil
import platform
from datetime import datetime
from api.send import send_private_msg, send_group_msg

logger = logging.getLogger("status")

class P_statusPlugin(Plugin):
    def __init__(self, bot):
        self.bot = bot
        
        logger.info("status 插件正在初始化")

    async def on_message(self, message):
        user_id = message['user_id']
        raw_message = message['raw_message']
        message_type = message.get('message_type', '')

        # 检测是否为管理员且消息内容为 "#系统状态"
        if self.bot.is_admin(user_id):
            if raw_message.strip() == "#系统状态":
                # 获取系统状态信息
                system_status = self.get_system_status()
                # 根据消息类型（群消息或好友消息）发送系统状态信息
                logger.info("p_status 插件准备发送系统状态信息：\n%s", system_status)  # 添加日志输出以确认消息内容

                if message_type == "group":
                    group_id = message['group_id']
                    send_group_msg(self.bot.base_url, group_id, system_status, self.bot.token)
                elif message_type == "private":
                    send_private_msg(self.bot.base_url, user_id, system_status, self.bot.token)

            elif raw_message.strip() == "#插件列表":
                # 获取插件列表信息
                plugin_list_info = self.get_plugin_list_info()
                # 根据消息类型（群消息或好友消息）发送插件列表信息
                logger.info("p_status 插件准备发送插件列表信息：\n%s", plugin_list_info)  # 添加日志输出以确认消息内容

                if message_type == "group":
                    group_id = message['group_id']
                    send_group_msg(self.bot.base_url, group_id, plugin_list_info, self.bot.token)
                elif message_type == "private":
                    send_private_msg(self.bot.base_url, user_id, plugin_list_info, self.bot.token)

    def get_system_status(self):
        """获取当前系统状态信息"""
        # 获取 CPU 占用百分比
        cpu_usage = psutil.cpu_percent(interval=1)
        # 获取 RAM 占用百分比和用量
        ram_info = psutil.virtual_memory()
        ram_usage_percent = ram_info.percent
        ram_usage_gb = ram_info.used / (1024 ** 3)
        ram_total_gb = ram_info.total / (1024 ** 3)
        
        # 获取当前 bot 版本
        bot_version = self.bot.bot_version
        
        # 获取当前系统时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建系统状态消息
        system_status = (
            f"系统状态：\n"
            f"▷  当前 CPU 占用: {cpu_usage}%\n"
            f"▷  当前 RAM 占用: {ram_usage_percent}% ({ram_usage_gb:.2f}GB/{ram_total_gb:.2f}GB)\n"
            f"▷  当前 bot 版本: {bot_version}\n"
            f"▷  当前系统时间: {current_time}\n"
        )
        
        return system_status

    def get_plugin_list_info(self):
        """获取插件列表信息"""
        # 获取插件信息
        folder_plugins = self.bot.pm_list.get("folder_plugins", {})
        file_plugins = self.bot.pm_list.get("file_plugins", {})

        # 格式化插件列表信息
        folder_plugins_info = "\n".join(
            f"📁 {name}: \n ▷  {'启用' if info['enable'] else '禁用'}, 版本 {info['version']}"
            for name, info in folder_plugins.items()
        )
        
        file_plugins_info = "\n".join(
            f"📄 {name}: \n ▷  {'启用' if info['enable'] else '禁用'}, 版本 {info['version']}"
            for name, info in file_plugins.items()
        )

        plugin_list_info = (
            f"插件列表：\n"
            f"文件夹插件：\n{folder_plugins_info if folder_plugins_info else '无'}\n\n"
            f"单文件插件：\n{file_plugins_info if file_plugins_info else '无'}"
        )

        return plugin_list_info
