# bot.py

import asyncio
import logging
import time
from fastapi import FastAPI, Request  # type: ignore
from plugin_manager import PluginManager
import json
import websockets
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

        #连接配置
        self.rtmsg_type = config.get("rtmsg_type", "http")  # 默认为 HTTP
        self.rq_type = config.get("rq_type", "http")  # 默认为 HTTP

        self.rt_http_prot = config.get("rt_http_prot", 18080)  # HTTP 上报消息接收端口
        self.rq_http_url = config.get("rq_http_url")    # HTTP api 请求地址

        self.r_ws_port = config.get("r_ws_port", 18081) # 反向 ws 端口
        self.f_ws_url = config.get("f_ws_url")  # 正向 ws 连接地址

        #临时兼容旧的连接配置
        self.base_url = config.get("rq_http_url")

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
        
        async def main():
            if self.rtmsg_type == "ws":
                task1 = asyncio.create_task(self.websocket_server())  # 启动 WebSocket 服务器
            else:
                task1 = asyncio.create_task(self.http_server())  # 启动 HTTP 服务器

            if self.rq_type == "ws":
                task2 = asyncio.create_task(self.reverse_websocket_server())  # 启动反向 WebSocket 服务器
            else:
                task2 = None

            tasks = [task1]
            if task2 is not None:
                tasks.append(task2)

            await asyncio.gather(*tasks)  # 并发运行所有任务

        asyncio.run(main())  # 启动主事件循环

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

    async def http_server(self):
        # 启动 HTTP 消息接收服务器
        logger.info("消息接收服务器启动中...")
        import uvicorn  # type: ignore
        config = uvicorn.Config(self.app, host="0.0.0.0", port=self.rt_http_prot, workers=4)
        server = uvicorn.Server(config)
        await server.serve()

    async def websocket_server(self):
        # 正向 WebSocket 消息接收服务器
        logger.info("消息接收服务器启动中...")
        logger.info(f"尝试连接到 WebSocket 地址: {self.f_ws_url}")
        try:
            async with websockets.connect(self.f_ws_url, extra_headers={"Authorization": f"Bearer {self.token}"}) as websocket:
                logger.info(f"\n\n成功连接到 WebSocket 地址: {self.f_ws_url}\n\n开始接收消息\n")
                while True:
                    message = await websocket.recv()  # 接收消息
                    
                    logger.debug(f"收到 WebSocket 消息原文: {message}")
                    
                    try:
                        # 将消息字符串转换为 JSON 数据
                        data = json.loads(message)
                        
                        # 格式化消息并输出到日志
                        extracted_info = self.extract_message_info(data)
                        logger.debug("\n- - -收到 WebSocket 消息- - -\n%s\n- -**- -**- -**- -", extracted_info)
                        
                        # 处理消息
                        await self.handle_message(data)
                    except json.JSONDecodeError:
                        logger.error("无法解析 WebSocket 消息的 JSON 数据")
                    except Exception as e:
                        logger.error(f"处理 WebSocket 消息时出错: {e}")

        except Exception as e:
            logger.error(f"WebSocket 连接失败: {e} \n\n5秒\n后重连")
            await asyncio.sleep(5)  # 等待5秒后重试
            await self.websocket_server()  # 重试连接

    def create_routes(self):
        # HTTP 接收消息后路由
        @self.app.post("/")
        async def root(request: Request):
            data = await request.json()
            extracted_info = self.extract_message_info(data)
            logger.info("\n- - -http事件：收到消息- - -\n%s\n- -**- -**- -**- -", extracted_info)
            await self.handle_message(data)
            return {}

    async def handle_message(self, message):
        # 分发消息给插件管理器
        if 'raw_message' not in message:
            if 'meta_event_type' in message:
                logger.debug(f"心跳事件")
                return
            else:
                logger.warning(f"消息丢失，可能被撤回")
                return
        
        semaphore = asyncio.Semaphore(200)  # 限制并发处理任务数量为200
        await self.plugin_manager.dispatch_message(message, semaphore)
