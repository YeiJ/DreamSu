class Plugin:
    def __init__(self, bot):
        self.bot = bot

    def on_message(self, message):
        raise NotImplementedError("子类(插件入口main.py)必须实现 on_message 方法")
