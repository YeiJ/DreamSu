import os
import yaml

from api.get import get_group_list

def update_group_list(self):
    # 获取群列表
    group_data = get_group_list(self.base_url, self.token)
    groups = {group['group_id']: group for group in group_data['data']}
    
    # 确保缓存文件夹存在
    os.makedirs('cache', exist_ok=True)
    
    # 定义文件路径
    file_path = 'cache/group_list.yml'
    
    # 如果文件存在，读取现有数据
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_groups = yaml.safe_load(file) or {}
    else:
        existing_groups = {}
    
    # 找出新增群组
    new_groups = {group_id: group for group_id, group in groups.items() if group_id not in existing_groups}
    
    # 找出已删除的群组
    removed_groups = {group_id: existing_groups[group_id] for group_id in existing_groups if group_id not in groups}
    
    # 更新现有群组列表
    existing_groups.update(groups)
    
    # 写入更新后的数据
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(existing_groups, file, allow_unicode=True)
    
    # 更新全局群列表
    self.group_list = list(groups.values())
    
    return new_groups, removed_groups, len(groups)
