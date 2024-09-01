import json
import logging
import os
from plugin_base import Plugin
from api.send import send_private_msg, send_group_msg

logger = logging.getLogger("p_keywordreply")

class P_keywordreplyPlugin(Plugin):
    def __init__(self, bot):
        self.bot = bot
        self.keywords_config = self.load_keywords_config()

        # 计算关键词数量并记录日志
        if "keywords_list" in self.keywords_config:
            keyword_count = sum(len(entry["keyword"]) if isinstance(entry["keyword"], list) else 1 for entry in self.keywords_config["keywords_list"])
            logger.info("加载了 %d 个关键词配置", keyword_count)
        else:
            logger.info("未找到关键词列表配置")

    def load_keywords_config(self):
        """加载关键词配置"""
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'keywords.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                logger.debug("加载关键词配置文件：%s", config_path)
                return json.load(f)
        except FileNotFoundError:
            logger.error("关键词配置文件未找到：%s", config_path)
            return {}

    def on_message(self, message):
        user_id = message['user_id']
        message_type = message.get('message_type', '')
        raw_message = message['raw_message']
        group_id = message.get('group_id', None)
        is_admin = self.bot.is_admin(user_id)

        logger.debug("收到消息: user_id=%s, message_type=%s, raw_message=%s, group_id=%s", user_id, message_type, raw_message, group_id)

        # 遍历关键词列表，检查每个关键词的触发条件
        for keyword_entry in self.keywords_config.get("keywords_list", []):
            if not keyword_entry.get("enable", False):
                logger.debug("关键词未启用，跳过: %s", keyword_entry.get("keyword"))
                continue
            
            keywords = keyword_entry["keyword"]  # keywords 现在是一个列表
            method = keyword_entry["method"]
            admin_need = keyword_entry["admin_need"]
            reply = keyword_entry["reply"]

            logger.debug("处理关键词: %s, method=%s, admin_need=%s", keywords, method, admin_need)

            # 检查管理员权限
            if admin_need and not is_admin:
                logger.debug("需要管理员权限，用户 %s 不是管理员，跳过", user_id)
                continue

            # 检查关键词匹配
            if method == "exact_match":
                match = any(raw_message == kw for kw in keywords)
            elif method == "fuzzy_match":
                match = any(kw in raw_message for kw in keywords)
            else:
                match = False

            logger.debug("关键词匹配结果: %s", match)

            if match:
                if message_type == 'group':
                    if self.check_group_limits(keyword_entry, group_id):
                        self.reply_in_group(group_id, user_id, reply, keyword_entry)
                elif message_type == 'private':
                    if self.check_private_limits(keyword_entry, user_id):
                        self.reply_in_private(user_id, reply)

    def check_group_limits(self, keyword_entry, group_id):
        """检查群组限制"""
        group_limits = keyword_entry.get("group_limits", {})
        if not group_limits.get("enable", False):
            logger.debug("群组限制未启用，允许发送消息")
            return True

        method = group_limits.get("method", "blacklist")
        group_ids = group_limits.get("group_ids", [])
        logger.debug("检查群组限制: method=%s, group_id=%s, group_ids=%s", method, group_id, group_ids)

        if method == "blacklist":
            result = group_id not in group_ids
        elif method == "whitelist":
            result = group_id in group_ids
        else:
            result = False

        logger.debug("群组限制检查结果: %s", result)
        return result

    def check_private_limits(self, keyword_entry, user_id):
        """检查私聊限制"""
        private_limits = keyword_entry.get("private_limits", {})
        if not private_limits.get("enable", False):
            logger.debug("私聊限制未启用，允许发送消息")
            return True

        method = private_limits.get("method", "blacklist")
        user_ids = private_limits.get("user_ids", [])
        logger.debug("检查私聊限制: method=%s, user_id=%s, user_ids=%s", method, user_id, user_ids)

        if method == "blacklist":
            result = user_id not in user_ids
        elif method == "whitelist":
            result = user_id in user_ids
        else:
            result = False

        logger.debug("私聊限制检查结果: %s", result)
        return result

    def reply_in_group(self, group_id, user_id, reply, keyword_entry):
        """在群组内进行回复"""
        atreply = keyword_entry["group_limits"].get("atreply", False)
        if atreply:
            reply = f"[CQ:at,qq={user_id}] {reply}"
        logger.debug("群组内发送回复: group_id=%s, reply=%s", group_id, reply)
        send_group_msg(self.bot.base_url, group_id, reply, self.bot.token)
        logger.info("群组 %s 内发送消息: %s", group_id, reply)

    def reply_in_private(self, user_id, reply):
        """在私聊中进行回复"""
        logger.debug("私聊内发送回复: user_id=%s, reply=%s", user_id, reply)
        send_private_msg(self.bot.base_url, user_id, reply, self.bot.token)
        logger.info("私聊发送消息给 %s: %s", user_id, reply)
