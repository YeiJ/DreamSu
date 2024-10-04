import os
import yaml

from api.get import get_friend_list

def update_friend_list(self):
    # 获取好友列表
    friend_data = get_friend_list(self.base_url, self.token)
    friends = {friend['user_id']: friend for friend in friend_data['data']}
    
    # 确保缓存文件夹存在
    os.makedirs('cache', exist_ok=True)
    
    # 定义文件路径
    file_path = 'cache/friend_list.yml'
    
    # 如果文件存在，读取现有数据
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_friends = yaml.safe_load(file) or {}
    else:
        existing_friends = {}
    
    # 找出新增好友
    new_friends = {uid: friend for uid, friend in friends.items() if uid not in existing_friends}
    
    # 找出已删除的好友
    removed_friends = {uid: existing_friends[uid] for uid in existing_friends if uid not in friends}
    
    # 更新现有好友列表
    existing_friends.update(friends)
    
    # 写入更新后的数据
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(existing_friends, file, allow_unicode=True)

    # 更新全局好友列表
    self.friend_list = list(friends.values())
    
    return new_friends, removed_friends, len(friends)
