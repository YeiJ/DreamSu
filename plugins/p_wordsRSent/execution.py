# plugins/p_wordsRSent/execution.py

import random
import time
import logging
from threading import Thread    
from api.send import send_msg

logger = logging.getLogger("p_wordsRSent")

class P_wordsRSentExecution:
    def __init__(self, bot, words_repo, rules):
        self.bot = bot
        self.words_repo = words_repo
        self.rules = rules

        self.loaded_rules = {}  # 加载的规则
        self.ignored_rules = []  # 忽略的规则
        self.unloaded_rules = []  # 未加载的规则

        # 添加日志：输出正在加载的规则信息
        logger.info("开始加载规则...")

        # 规则类型映射
        rule_type_map = {
            'scheduled_message': '定时任务',
            'group_message_keyword_reply': '关键词回复'
        }

        for rule_name, rule in rules.items():
            if rule_name.startswith('r_'):
                # 加载 r_ 开头的规则
                self.loaded_rules[rule_name] = rule
                rule_type = rule.get('type', '未知类型')
                # 根据 rule_type 显示相应的描述文本
                rule_description = rule_type_map.get(rule_type, '未知类型')
                logger.info(f"加载规则: {rule_name} (类型: {rule_description})")
            elif rule_name.startswith('u_'):
                # 放入未加载规则列表
                self.unloaded_rules.append(rule_name)
                logger.info(f"未加载规则: {rule_name}")
            else:
                # 放入忽略列表
                self.ignored_rules.append(rule_name)
                logger.info(f"忽略规则: {rule_name}")

        # 输出规则分类信息
        logger.info(f"已加载的规则: {self.loaded_rules.keys()}")
        logger.info(f"未加载的规则: {self.unloaded_rules}")
        logger.info(f"忽略的规则: {self.ignored_rules}")

        self.start_scheduled_rules()

    def on_message(self, message):
        """Handle incoming messages."""
        message_type = message['message_type']
        content = message['raw_message']

        # Process message based on rules
        if message_type == 'group':
            group_id = message['group_id']
            for rule_name, rule in self.rules.items():
                if rule.get('type') == 'group_message_keyword_reply':
                    if content in rule['keywords'] and group_id in rule.get('group_list', []):
                        logger.info(f"关键词触发发送群组目标: {group_id} \n发送规则: {rule}")
                        self.send_random_words(group_id, rule)
        elif message_type == 'private':
            user_id = message['user_id']
            for rule_name, rule in self.rules.items():
                if rule.get('type') == 'private_message_keyword_reply':
                    if content in rule['keywords']:
                        logger.info(f"关键词触发发送私聊目标: {user_id} \n发送规则: {rule}")
                        self.send_random_words(user_id, rule)

    def send_random_words(self, target_id, rule):
        """Send random words to a target based on a rule."""
        repo_files = rule.get('word_repos', [])
        num_words = rule.get('word_quantity', 5)
        all_words = []  # 用于存放所有仓库中的词条
        
        # 合并所有仓库中的词条
        for repo_file in repo_files:
            words = self.words_repo.get(repo_file, [])
            if words:
                logger.info(f"从仓库文件 {repo_file} 中获取到 {len(words)} 个词条。")
                all_words.extend(words)

        # 从所有词条中随机抽取指定数量的词条
        selected_words = random.sample(all_words, min(num_words, len(all_words)))

        if selected_words:
            current_time = time.strftime("%H:%M")
            message = f"当前时间: \n {current_time}\n本次的 {len(selected_words)} 个随机词条为：\n\n" + "\n".join(["▷ " + word for word in selected_words])
            logger.info(f"准备发送消息到 {target_id}，内容: {message}")

            # 根据 target_id 来判断发送类型是群聊还是私聊
            message_type = "group" if target_id in rule.get('group_list', []) else "private"

            try:
                send_msg(self.bot.base_url, message_type, target_id, message, self.bot.token)
                logger.info(f"已发送消息到 {target_id}，内容包含 {len(selected_words)} 个词条。")
            except Exception as e:
                logger.error(f"发送消息失败: {e}, 规则: {rule}, 目标ID: {target_id}")
        else:
            logger.warning(f"未能从仓库中选取到词条，目标ID: {target_id}")


    def execute_scheduled_rules(self):
        """Execute scheduled rules at specified times."""
        time.sleep(3)  # 初始等待3秒
        while True:
            start_time = time.time()  # 记录循环开始时间
            current_time = time.strftime("%H:%M")
            # logger.info(f"\n##\n##当前时间: {current_time} - 正在检查定时任务...\n##\n")
            
            for rule_name, rule in self.rules.items():
                if rule.get('type') == 'scheduled_message' and current_time in rule.get('times', []):
                    logger.info(f"##执行定时任务: {rule_name}")
                    
                    # 处理群组目标
                    target_groups = rule.get('group_list', [])
                    logger.info(f"##定时任务发送群组列表: {target_groups} ")
                    for group_id in target_groups:
                        logger.info(f"##定时任务发送群组目标: {group_id} \n发送规则: {rule}")
                        self.send_random_words(group_id, rule)
                        time.sleep(3)  # 等待3秒发送下一条消息
                    
                    # 处理朋友目标
                    target_friends = rule.get('friend_list', [])
                    logger.info(f"##定时任务发送朋友列表: {target_friends} ")
                    for friend_id in target_friends:
                        logger.info(f"##定时任务发送朋友目标: {friend_id} \n发送规则: {rule}")
                        self.send_random_words(friend_id, rule)
                        time.sleep(3)  # 等待3秒发送下一条消息

            # 计算已经使用的时间
            elapsed_time = time.time() - start_time
            # 确定剩余的等待时间
            sleep_time = max(60 - elapsed_time, 0)
            # logger.info(f"##循环结束，等待 {sleep_time} 秒再继续...")
            time.sleep(sleep_time)  # 等待到下一个循环




    def start_scheduled_rules(self):
        """Start a thread to execute scheduled rules."""
        Thread(target=self.execute_scheduled_rules, daemon=True).start()
