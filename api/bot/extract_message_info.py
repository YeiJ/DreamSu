# bot/api/extract_message_info.py

#消息解析方法

import logging
from api.get import get_group_info

logger = logging.getLogger("DreamSu")

def extract_message_info(self, message):
    # 提取用户信息
    sender = message.get('sender', {})
    user_id = sender.get('user_id', '未知用户')
    message_id = message.get('message_id', '未知消息ID')
    nickname = sender.get('nickname', '未知昵称')
    card = sender.get('card', "未知名片")
    role = sender.get('role', '未知群员身份')
    message_type = message.get('message_type', '未知类型')
    raw_message = message.get('raw_message', '')
    group_id = message.get('group_id', '未知群ID')
    group_info = None   

    result = None  # 确保 result 被初始化

    # 提取消息内容
    message_content = []

    # 处理 meta_event 类型的消息
    if message.get('post_type') == 'meta_event':
        meta_event_type = message.get('meta_event_type', '未知事件类型')

        if meta_event_type == 'heartbeat':
            status = message.get('status', {})
            online_status = status.get('online', '未知在线状态')
            good_status = status.get('good', '未知健康状态')
            interval = message.get('interval', '未知心跳间隔')

            result = (
                f"[心跳事件] "
                f"在线状态: {online_status} "
                f"健康状态: {good_status} "
                f"心跳间隔: {interval} ms"
            )
            message_content.append(result)

        elif meta_event_type == 'lifecycle':
            sub_type = message.get('sub_type', '未知子类型')

            result = (
                "[生命周期事件] "
                f"子类型: {sub_type}"
            )
            message_content.append(result)

        return '\n'.join(message_content)  # 直接返回 meta_event 消息的内容

    #消息类型判断
    if message.get('post_type') == 'notice':
        notice_type = message.get('notice_type', '未知通知类型')
        
        if notice_type == 'group_recall':
            operator_id = message.get('operator_id', '未知操作用户ID')
            user_id = message.get('user_id', '未知用户ID')
            group_id = message.get('group_id', '未知群ID')
            message_id = message.get('message_id', '未知消息ID')

            group_info = next((group for group in self.group_list if group['group_id'] == group_id), None)
            logger.debug(f"获取的 group_info: {group_info}")  
            
            if group_info is None:
                logger.debug("group_info 为 None，无法提取信息")  
                group_name = '#'
            else:
                group_name = group_info.get('group_name', '未找到群名称')

            result = (
                f"[群消息撤回] "
                f"操作用户ID: {operator_id} "
                f"被撤回用户ID: {user_id} "
                f"群ID: {group_id} "
                f"群名称: {group_name} "
                f"被撤回消息ID: {message_id}"
            )
            message_content.append(result)

        elif notice_type == 'friend_recall':
            user_id = message.get('user_id', '未知用户ID')
            message_id = message.get('message_id', '未知消息ID')

            result = (
                f"[好友消息撤回] "
                f"用户ID: {user_id} "
                f"被撤回消息ID: {message_id}"
            )
            message_content.append(result)

        elif notice_type == 'group_increase':
            operator_id = message.get('operator_id', '未知群管理员用户ID')
            sub_type = message.get('sub_type', '未知操作类型')
            group_id = message.get('group_id', '未知群ID')
            user_id = message.get('user_id', '未知用户ID')

            result = (
                f"[新成员入群] "
                f"操作用户ID: {operator_id} "
                f"操作类型: {sub_type} "
                f"群ID: {group_id} "
                f"新成员用户ID: {user_id}"
            )
            message_content.append(result)

        else:
            message_content.append(f"未知通知类型: {notice_type}")
            return f"[原始消息内容] \n {message}"


    elif 'message' in message:
        for item in message['message']:
            data = item.get('data', {})
            content_type = item.get('type', '未知类型')
            if content_type == 'text':
                message_content.append(data.get('text', ''))
                # return f"原始消息内容: \n {message}"
            elif content_type == 'at':
                at_info = f"@{data.get('name', '未知用户')} (QQ: {data.get('qq', '未知QQ号')})"
                message_content.append(at_info)
            elif content_type == 'image':
                image_info = f"图片: {data.get('file', '未知文件名')} ({data.get('file_size', '未知大小')} bytes)"
                message_content.append(image_info)
            elif content_type == 'video':
                video_info = f"视频: {data.get('file', '未知文件名')} ({data.get('file_size', '未知大小')} bytes)"
                message_content.append(video_info)
            elif content_type == 'record':
                voice_info = f"语音: {data.get('file', '未知文件名')} ({data.get('file_size', '未知大小')} bytes)"
                message_content.append(voice_info)
            elif content_type == 'file':
                file_info = f"文件: {data.get('file', '未知文件名')} ({data.get('file_size', '未知大小')} bytes)"
                message_content.append(file_info)
            elif content_type == 'face':
                face_info = f"表情: {data.get('id', '未知ID')}"
                message_content.append(face_info)
            elif content_type == 'forward':
                forward_info = f"转发消息ID: {data.get('id', '未知ID')}"
                message_content.append(forward_info)
            elif content_type == 'reply':
                reply_info = f"回复消息ID: {data.get('id', '未知ID')}"
                message_content.append(reply_info)
            else:
                message_content.append(f"未知内容类型: {content_type}")
                return f"原始消息内容: \n {message}"

    # 检查是否为主人消息
    admin_marker = ""
    if self.is_admin(user_id):
        admin_marker = "\033[1;33m ༺ཌༀMasterༀད༻ \033[0m" 

    # 消息类型映射
    message_type_map = {
        'private': '私聊消息',
        'group': '群聊消息'
    }

    message_type_description = message_type_map.get(message_type, '未知类型')

    if message_type == 'group':

        group_info = next((group for group in self.group_list if group['group_id'] == group_id), None)

        if group_info is None:
            # 处理 group_info 为 None 的情况
            logger.debug(f"获取的 group_info: {group_info}")
            logger.debug("group_info 为 None，无法提取信息")
            group_name = 'group_info 为 None'
        else:
            logger.debug(f"获取的 group_info: {group_info}")
            group_name = group_info.get('group_name', '未找到群名称')  
            
        #是否有群名片
        if card:
            nickname = nickname + f"(群名片：{card})"

        # 消息类型映射
        role_type_map = {
            'member': '普通群员',
            'owner': '\033[1m群主\033[0m',
            'admin': '\033[1m管理员\033[0m',
            None: '未知身份'
        } 

        role_type_description = role_type_map.get(role, '未知身份')
        nickname = role_type_description + " || " + nickname

        # 格式化输出
        result = (
            f"[ \033[44m{message_type_description}\033[0m ] "   # 消息类型
            f"  {group_name} ( \033[36m{group_id}\033[0m ) 消息ID: {message_id}\n"    # 群聊信息
            f"|| {nickname} (ID: {user_id}) ] {admin_marker}\n" # 用户信息
            f">> {' '.join(message_content) or raw_message}\n" # 内容
        )
    elif message_type == 'private':
        # 格式化输出
        result = (
            f"[ \033[44m{message_type_description}\033[0m ] "   # 消息类型
            f"|| {nickname} (ID: {user_id}) 消息ID: {message_id}  {admin_marker}\n" # 用户信息
            f">> {' '.join(message_content) or raw_message}\n" # 内容
        )

    return result
