# bot/api/is_group_admin.py

from api.get import get_group_member_info

def is_group_admin(self, group_id, user_id):
    """
    检查给定的 user_id 是否是指定群的群管。
    """
    group_member_info = get_group_member_info(self.base_url, group_id, user_id, False, self.token)

    # 检查响应状态
    if group_member_info is None or group_member_info['status'] != 'ok' or group_member_info['retcode'] != 0:
        return False  # 请求失败，返回 False

    # 获取角色信息
    role = group_member_info['data'].get('role', '')

    # 判断是否为群管或以上权限
    return role in ['owner', 'admin']
