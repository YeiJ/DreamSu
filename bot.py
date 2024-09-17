# bot.py

import asyncio
import logging
import time
from fastapi import FastAPI, Request  # type: ignore
from plugin_manager import PluginManager
import os
import importlib.util  # 用于动态加载模块
import inspect  # 用于检查模块内的函数

# 配置日志
logger = logging.getLogger("DreamSu")

class Bot:
    def __init__(self):

        # 动态加载 API 方法
        # self.load_api_methods('api') 禁止这样做
        self.load_api_methods('api/bot')

        # 导入配置文件
        config = self.load_config("config/config.json")
        dreamsu = self.load_config("config/DreamSu.json")
        
        self.bot_version = dreamsu.get("bot_version")
        self.rtmsg_prot = config.get("rtmsg_prot")
        self.base_url = config.get("base_url")
        self.token = config.get("token")
        
        # 实例化插件管理器
        self.plugin_manager = PluginManager(self)
        
        self.pm_status = 1  # 插件管理状态
        self.pm_list = {}   # 插件列表

        # 读取配置文件中的主人ID
        self.master_ids = config.get('masters', [])
        
        # 初始化FastAPI
        self.app = FastAPI()

        # 增加消息队列
        self.message_queue = asyncio.Queue()

        self.create_routes()

    def start(self):
        logger.info("DreamSuOB启动中...")
        logger.info(f"\n\n\n当前版本: {self.bot_version}\n\n")
        logger.info(f"主人账号: {self.master_ids}")
        logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-||")
        self.plugin_manager.load_plugins('plugins', 'plugins/example')  # 加载插件
        asyncio.run(self.run_server())  # 启动服务器

    def load_api_methods(self, directory):
        """动态加载指定目录下的所有.py文件中的函数，并将其添加到当前类的实例"""
        logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-||")
        if directory == "api":
            logger.info("正在加载OBv11方法...")
        else:
            logger.info("正在加载框架内部方法...")
        logger.debug(" ")
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                module_name = filename[:-3]  # 去掉".py"后缀
                file_path = os.path.join(directory, filename)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                except Exception as e:
                    logger.error(f"加载模块 {module_name} 失败: {e}")
                    continue

                # 获取模块中的所有函数并添加到当前类的实例中
                for name, func in inspect.getmembers(module, inspect.isfunction):
                    setattr(self, name, func.__get__(self))
                    
                    # 添加Debug日志来输出每个成功加载的方法名
                    logger.debug(f"成功加载方法: {name} 来自模块: {module_name}")

        if directory == "api":
            logger.info("OBv11方法加载完毕")
        else:
            logger.info("框架内部方法加载完毕")
        logger.info("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-||")

    async def run_server(self):
        logger.info("消息接收服务器启动中...")
        import uvicorn  # type: ignore
        config = uvicorn.Config(self.app, host="0.0.0.0", port=self.rtmsg_prot, workers=4)
        server = uvicorn.Server(config)
        await server.serve()

    def create_routes(self):
        @self.app.post("/")
        async def root(request: Request):
            data = await request.json()
            extracted_info = self.extract_message_info(data)
            logger.info("\n- - -收到消息- - -\n%s\n- -**- -**- -**- -", extracted_info)
            await self.handle_message(data)
            return {}

    async def handle_message(self, message):
        if 'raw_message' not in message:
            logger.warning(f"消息丢失，可能被撤回")
            return 
        
        semaphore = asyncio.Semaphore(200)  # 限制并发处理任务数量为200
        await self.plugin_manager.dispatch_message(message, semaphore)
