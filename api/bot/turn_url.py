from api.get import get_msg

def turn_url(self, message_id):
    # 获取消息 JSON
    json_data = get_msg(self.base_url, message_id, self.token) # type: ignore
    
    # 用于存储所有 image 类型的 data 字典的列表
    image_data_list = []

    # 检查 JSON 数据是否包含 'message' 键
    if 'message' in json_data:
        # 遍历消息中的每个部分
        for part in json_data['message']:
            # 检查消息类型是否为 'image'
            if part['type'] == 'image':
                # 提取 'data' 部分并添加到列表中
                image_data_list.append(part['data'])

    return image_data_list
