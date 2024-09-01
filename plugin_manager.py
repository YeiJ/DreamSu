import os
import importlib
import logging
import json
import time

logger = logging.getLogger("bot")

class PluginManager:
    def __init__(self, bot):
        self.bot = bot
        self.plugins = {
            "folder_plugins": {},
            "file_plugins": {},
            "loaded_plugins": []
        }  # 用于存储插件信息
        self.unloaded_plugins = []  # 用于存储未加载的插件名
        self.failedloaded_plugins = []  # 用于存储加载失败的插件名
        self.bot.pm_status = 1  # 插件管理器加载状态，默认值为1

    def load_plugins(self, folder_plugin_folder, file_plugin_folder):
        """加载插件，包括文件夹插件和单文件插件"""
        logger.info("正在启动插件管理器...")

        # 确保文件夹路径是存在的
        if not os.path.isdir(folder_plugin_folder):
            logger.info(f"Error: The folder '{folder_plugin_folder}' does not exist.")
            return

        if not os.path.isdir(file_plugin_folder):
            logger.info(f"Error: The folder '{file_plugin_folder}' does not exist.")
            return

        # 忽略的文件和文件夹列表
        ignore_files = {"__init__.py", "__pycache__"}

        # 加载文件夹插件
        time.sleep(1)
        self._load_folder_plugins(folder_plugin_folder, ignore_files)

        # 加载单文件插件
        time.sleep(1)
        self._load_file_plugins(file_plugin_folder, ignore_files)

        # 生成一个可序列化的插件字典，只保留插件的基本信息
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

        # 将可序列化的插件信息写入 JSON 配置文件
        with open("config/plugins.json", "w", encoding="utf-8") as f:
            json.dump(serializable_plugins, f, ensure_ascii=False, indent=4)

        # 更新 Bot 实例中的插件列表，仅保留基本信息
        self.bot.pm_list = serializable_plugins

        # 更新插件加载状态
        if not self.unloaded_plugins:
            logger.info("-----------------------------||")
            logger.info("✔️ 所有插件均已成功加载")
            logger.info("-----------------------------||")
        else:
            logger.info("▷▷--------------------------||")
            if self.unloaded_plugins and (not self.failedloaded_plugins):
                logger.info("📋 已卸载的插件名单: %s", ', '.join(self.unloaded_plugins))
                logger.info("-----------------------------||")
            elif self.failedloaded_plugins and (not self.unloaded_plugins):
                logger.info("❌ 加载失败的插件名单: %s", ', '.join(self.failedloaded_plugins))
                logger.info("-----------------------------||")
            elif self.unloaded_plugins and self.failedloaded_plugins:
                logger.info("📋 已卸载的插件名单: %s", ', '.join(self.unloaded_plugins))
                logger.info("-----------------------------||")
                logger.info("❌ 加载失败的插件名单: %s", ', '.join(self.failedloaded_plugins))
                logger.info("-----------------------------||")

        
        self.bot.pm_status = 2  # 加载完毕

    def _load_folder_plugins(self, folder_plugin_folder, ignore_files):
        logger.info("▷▷--------------------------||")
        logger.info("📋 加载文件夹插件目录: %s", folder_plugin_folder)
        logger.info("-----------------------------")
        
        for filename in os.listdir(folder_plugin_folder):
            folder_path = os.path.join(folder_plugin_folder, filename)

            # 排除特定文件夹
            if filename in ignore_files or not os.path.isdir(folder_path):
                continue

            # 只处理以 "p_" 或 "u_" 开头的文件夹
            if not (filename.startswith("p_") or filename.startswith("u_")):
                continue

            # 处理版本号
            if filename.startswith("p_") or filename.startswith("u_"):
                version = self._get_plugin_version(folder_path)
            
            # 记录插件信息
            self.plugins["folder_plugins"][filename] = {
                "enable": filename.startswith("p_"),
                "version": version
            }

            # 尝试加载插件
            if filename.startswith("p_"):
                module_path = f"plugins.{filename}.main"
                if self._load_plugin(module_path, filename):
                    logger.info("✔️ 插件📁 %s 加载成功", filename)
                    logger.info("⚡ 当前插件版本号为 %s", version)
                    logger.info("-----------------------------")
        
                else:
                    self.failedloaded_plugins.append("📁 " + filename)
                    logger.info("💡 插件📁 %s 加载失败", filename)
                    logger.info("-----------------------------")
            elif filename.startswith("u_"):
                self.unloaded_plugins.append("📁 " + filename)
                logger.info("🗑️ 文件夹插件📁 %s 已卸载", filename)

    def _load_file_plugins(self, file_plugin_folder, ignore_files):
        logger.info("▷▷--------------------------||")
        logger.info("📋 加载单文件插件目录: %s", file_plugin_folder)
        logger.info("-----------------------------")
        
        for filename in os.listdir(file_plugin_folder):
            file_path = os.path.join(file_plugin_folder, filename)

            # 跳过非Python文件或特殊文件
            if filename in ignore_files or not filename.endswith(".py") or filename.startswith("_"):
                continue

            plugin_name = filename[:-3]

            # 跳过以"u_"开头的单文件插件
            if plugin_name.startswith("u_"):
                version = self._get_plugin_version(file_path)
                self.plugins["file_plugins"][filename] = {
                    "enable": False,
                    "version": version
                }
                self.unloaded_plugins.append("📄 " + plugin_name)
                logger.info("🗑️ 插件📄 %s 处于卸载状态", plugin_name)
                continue

            # 检查插件名是否以"p_"开头
            if plugin_name.startswith("p_"):
                version = self._get_plugin_version(file_path)
                self.plugins["file_plugins"][filename] = {
                    "enable": True,
                    "version": version
                }
                module_path = f"plugins.example.{plugin_name}"
                if self._load_plugin(module_path, plugin_name):
                    logger.info("✔️ 插件📄 %s 加载成功", plugin_name)
                    logger.info("⚡ 当前插件版本号为 %s", version)
                    logger.info("-----------------------------")
                else:
                    self.failedloaded_plugins.append("📄 " + plugin_name)
                    logger.info("💡 插件📄 %s 加载失败，已添加到加载失败列表", plugin_name)
                    logger.info("-----------------------------")

    def _load_plugin(self, module_path, plugin_name):
        """尝试加载插件模块并实例化插件类"""
        if plugin_name in [plugin.__class__.__name__ for plugin in self.plugins.get("loaded_plugins", [])]:
            logger.warning("插件 %s 已经加载，跳过重复加载。", plugin_name)
            return False
        try:
            module = importlib.import_module(module_path)
            plugin_class = self._get_plugin_class(module, plugin_name)
            if plugin_class:
                plugin_instance = plugin_class(self.bot)
                self.plugins.setdefault("loaded_plugins", []).append(plugin_instance)  # 确保插件实例添加到 `loaded_plugins`
                return True
            else:
                logger.error("❌ 无法在模块 %s 中找到插件类 %s", module_path, plugin_name.capitalize())
                return False
        except ModuleNotFoundError as e:
            logger.error("❌ 模块未找到 %s: %s", module_path, e)
        except AttributeError as e:
            logger.error("❌ 插件类不存在 %s: %s", plugin_name.capitalize(), e)
        except Exception as e:
            logger.error("❌ 加载插件 %s 失败: %s", plugin_name, e)
        return False


    def _get_plugin_class(self, module, plugin_name):
        """从模块中获取插件类，尝试大写或小写形式"""
        class_name = f"{plugin_name.capitalize()}Plugin"
        if hasattr(module, class_name):
            return getattr(module, class_name)
        else:
            # 尝试小写形式
            class_name = f"{plugin_name.lower()}Plugin"
            if hasattr(module, class_name):
                return getattr(module, class_name)
        return None

    def _get_plugin_version(self, plugin_path):
        version = "未知版本"
        
        if os.path.isfile(plugin_path):
            # 读取文件插件的版本信息，假设在第二行
            with open(plugin_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:  # 确保至少有两行
                    line = lines[1].strip()
                    if line.startswith('# __version__'):
                        version = line.split('=')[1].strip().strip('"').strip("'")
                        
        elif os.path.isdir(plugin_path):
            # 读取文件夹插件的版本信息，假设在 __init__.py 的第二行
            init_file = os.path.join(plugin_path, '__init__.py')
            if os.path.isfile(init_file):
                with open(init_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 1:  # 确保至少有两行
                        line = lines[1].strip()
                        if line.startswith('# __version__'):
                            version = line.split('=')[1].strip().strip('"').strip("'")
        
        return version

    def dispatch_message(self, message):
        # logger.info("Dispatching message to plugins: %s", message)
        for plugin in self.plugins.get("loaded_plugins", []):
            if hasattr(plugin, 'on_message'):  # 检查插件是否具有 on_message 方法
                plugin.on_message(message)
            else:
                logger.warning("插件 %s 缺少 on_message 方法", plugin)
