# plugins/p_wordsRSent/main.py

from plugin_base import Plugin
import logging
import os
import json
from .admin import P_wordsRSentAdmin
from .execution import P_wordsRSentExecution

logger = logging.getLogger("p_wordsRSent")

class P_wordsrsentPlugin(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.words_repo = {}
        self.config = {}
        self.rules = {}
        self.load_config()
        self.load_words_repo()
        self.load_rules()

        # 初始化后台管理模块和规则执行模块
        self.execution = P_wordsRSentExecution(bot, self.words_repo, self.rules)
        # 暂时禁用 admin 模块
        # self.admin = P_wordsRSentAdmin(bot, self.words_repo, self.rules, self.config)

    def load_config(self):
        """Load configuration from config.json."""
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logger.info("配置文件加载完毕")
        except Exception as e:
            logger.error(f"配置文件加载失败:\n {e}")

    def load_words_repo(self):
        """Load enabled word repositories."""
        repo_path = os.path.join(os.path.dirname(__file__), 'repo')
        for file_name in os.listdir(repo_path):
            if file_name.startswith('r_') and file_name.endswith('.yml'):
                with open(os.path.join(repo_path, file_name), 'r', encoding='utf-8') as f:
                    self.words_repo[file_name] = f.readlines()
        logger.info(f"从仓库文件: {list(self.words_repo.keys())} 中加载词库")

    def load_rules(self):
        """Load rules from rules.json."""
        rules_path = os.path.join(os.path.dirname(__file__), 'config', 'rules.json')
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
            logger.info("规则列表加载完毕")
        except Exception as e:
            logger.error(f"规则列表加载失败: \n{e}")

    async def on_message(self, message):
        self.execution.on_message(message)  # 调用执行器的 on_message 方法