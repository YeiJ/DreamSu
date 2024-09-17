# plugin_manager.py

import os
import importlib
import logging
import json
import asyncio

logger = logging.getLogger("bot")

class PluginManager:
    def __init__(self, bot):
        self.bot = bot
        self.plugins = {
            "folder_plugins": {},
            "file_plugins": {},
            "loaded_plugins": []
        }  # 用于存储插件信息
        self.unloaded_plugins = []  # 未加载的插件
        self.failedloaded_plugins = []  # 加载失败的插件
        self.bot.pm_status = 1  # 插件管理器加载状态

    def load_plugins(self, folder_plugin_folder, file_plugin_folder):
        """加载插件，包括文件夹插件和单文件插件"""
        logger.info("正在启动插件管理器...")

        # 检查插件目录是否存在
        if not os.path.isdir(folder_plugin_folder) or not os.path.isdir(file_plugin_folder):
            logger.error("插件文件夹路径错误")
            return

        # 忽略文件列表
        ignore_files = {"__init__.py", "__pycache__"}

        # 启动一个事件循环来运行异步任务
        loop = asyncio.get_event_loop()

        if loop.is_running():
            # 如果事件循环已经运行，直接创建任务
            asyncio.create_task(self._load_folder_plugins(folder_plugin_folder, ignore_files))
            asyncio.create_task(self._load_file_plugins(file_plugin_folder, ignore_files))
        else:
            # 否则，启动新的事件循环并运行任务
            loop.run_until_complete(asyncio.gather(
                self._load_folder_plugins(folder_plugin_folder, ignore_files),
                self._load_file_plugins(file_plugin_folder, ignore_files)
            ))

        # 生成插件的可序列化版本，仅保留插件的基本信息
        serializable_plugins = {
            "folder_plugins": {
                name: {"enable": data["enable"], "version": data["version"]}
                for name, data in self.plugins["folder_plugins"].items()
            },
            "file_plugins": {
                name: {"enable": data["enable"], "version": data["version"]}
                for name, data in self.plugins["file_plugins"].items()
            }
        }

        # 将插件信息写入 JSON 文件
        with open("config/plugins.json", "w", encoding="utf-8") as f:
            json.dump(serializable_plugins, f, ensure_ascii=False, indent=4)

        # 更新 Bot 实例中的插件列表
        self.bot.pm_list = serializable_plugins

        # 插件加载状态日志
        if not self.unloaded_plugins:
            logger.info("-----------------------------||")
            logger.info("✔️ 所有插件均已成功加载")
            logger.info("-----------------------------||")
        else:
            logger.info("▷▷--------------------------||")
            if self.unloaded_plugins and not self.failedloaded_plugins:
                logger.info("📋 已卸载的插件名单: %s", ', '.join(self.unloaded_plugins))
                logger.info("-----------------------------||")
            elif self.failedloaded_plugins and not self.unloaded_plugins:
                logger.info("❌ 加载失败的插件名单: %s", ', '.join(self.failedloaded_plugins))
                logger.info("-----------------------------||")
            elif self.unloaded_plugins and self.failedloaded_plugins:
                logger.info("📋 已卸载的插件名单: %s", ', '.join(self.unloaded_plugins))
                logger.info("-----------------------------||")
                logger.info("❌ 加载失败的插件名单: %s", ', '.join(self.failedloaded_plugins))
                logger.info("-----------------------------||")

        self.bot.pm_status = 2  # 加载完成

    async def _load_folder_plugins(self, folder_plugin_folder, ignore_files):
        logger.info(f"加载文件夹插件目录: {folder_plugin_folder}")
        for filename in os.listdir(folder_plugin_folder):
            folder_path = os.path.join(folder_plugin_folder, filename)

            if filename in ignore_files or not os.path.isdir(folder_path):
                continue

            if not (filename.startswith("p_") or filename.startswith("u_")):
                continue

            version = self._get_plugin_version(folder_path)
            self.plugins["folder_plugins"][filename] = {
                "enable": filename.startswith("p_"),
                "version": version
            }

            if filename.startswith("p_"):
                module_path = f"plugins.{filename}.main"
                if await self._load_plugin(module_path, filename):
                    logger.info(f"✔️ 插件📁 {filename} 加载成功，版本 {version}")
                else:
                    self.failedloaded_plugins.append(filename)
                    logger.error(f"❌ 插件 {filename} 加载失败")

    async def _load_file_plugins(self, file_plugin_folder, ignore_files):
        logger.info(f"加载单文件插件目录: {file_plugin_folder}")
        for filename in os.listdir(file_plugin_folder):
            if filename in ignore_files or not filename.endswith(".py"):
                continue

            plugin_name = filename[:-3]
            if plugin_name.startswith("u_"):
                version = self._get_plugin_version(os.path.join(file_plugin_folder, filename))
                self.plugins["file_plugins"][filename] = {
                    "enable": False,
                    "version": version
                }
                self.unloaded_plugins.append(plugin_name)
                logger.info(f"🗑️ 插件📄 {plugin_name} 处于卸载状态")
                continue

            version = self._get_plugin_version(os.path.join(file_plugin_folder, filename))
            self.plugins["file_plugins"][filename] = {
                "enable": True,
                "version": version
            }

            module_path = f"plugins.example.{plugin_name}"
            if await self._load_plugin(module_path, plugin_name):
                logger.info(f"✔️ 插件📄 {plugin_name} 加载成功，版本 {version}")
            else:
                self.failedloaded_plugins.append(plugin_name)
                logger.error(f"❌ 插件📄 {plugin_name} 加载失败")

    async def _load_plugin(self, module_path, plugin_name):
        """加载插件并实例化插件类"""
        if plugin_name in [plugin.__class__.__name__ for plugin in self.plugins["loaded_plugins"]]:
            logger.warning(f"插件 {plugin_name} 已加载，跳过重复加载。")
            return False
        try:
            module = importlib.import_module(module_path)
            plugin_class = self._get_plugin_class(module, plugin_name)
            if plugin_class:
                plugin_instance = plugin_class(self.bot)
                self.plugins["loaded_plugins"].append(plugin_instance)
                return True
        except Exception as e:
            logger.error(f"加载插件 {plugin_name} 时出错: {e}")
        return False

    def _get_plugin_class(self, module, plugin_name):
        """从模块中获取插件类"""
        class_name = f"{plugin_name.capitalize()}Plugin"
        return getattr(module, class_name, None)

    def _get_plugin_version(self, plugin_path):
        """获取插件版本"""
        version = "未知版本"
        if os.path.isfile(plugin_path):
            with open(plugin_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1 and lines[1].startswith('# __version__'):
                    version = lines[1].split('=')[1].strip().strip('"').strip("'")
        elif os.path.isdir(plugin_path):
            init_file = os.path.join(plugin_path, '__init__.py')
            if os.path.isfile(init_file):
                with open(init_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 1 and lines[1].startswith('# __version__'):
                        version = lines[1].split('=')[1].strip().strip('"').strip("'")
        return version
    
    async def dispatch_message(self, message, semaphore):
        """异步分发消息"""
        async with semaphore:
            tasks = []
            for plugin in self.plugins.get("loaded_plugins", []):
                if hasattr(plugin, 'on_message'):
                    try:
                        tasks.append(asyncio.create_task(plugin.on_message(message)))  # 并行处理插件消息
                    except Exception as e:
                        logger.error(f"插件处理消息时出错: {e}")
            if tasks:
                await asyncio.gather(*tasks)  # 并发执行所有插件的 on_message
