# 此人是否在目标群内

import logging
from api.get import get_group_member_list

logger = logging.getLogger("DreamSu")

def is_target_in_group(self, user_id, group_id):
    try:
        member_list_response = get_group_member_list(self.base_url, group_id, self.token)
        
        # 检查响应状态
        if member_list_response['status'] != 'ok' or member_list_response['retcode'] != 0:
            logger.error(f"[ is_target_in_group ] 获取群成员数据失败，状态: {member_list_response['status']}, 错误码: {member_list_response['retcode']}")
            return False
        
        member_list = member_list_response['data']  # 提取成员列表
        logger.debug("[ is_target_in_group ] 获取的群成员列表成功")
        # logger.debug(f"[ is_target_in_group ] 获取的群成员列表: {member_list}")

    except Exception as e:
        logger.error(f"[ is_target_in_group ] 获取群成员数据时出现错误: {e}")
        return False  # 返回 False 以处理错误

    if not isinstance(member_list, list):
        logger.error(f"[ is_target_in_group ] 获取的群成员列表格式不正确: {member_list_response}")
        return False

    for member in member_list:
        if member['user_id'] == user_id:
            return True
    return False
