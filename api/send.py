import requests
import logging

logger = logging.getLogger("api.send")

#发送私聊消息
def send_private_msg(base_url, target_qq, message, token=None):
    """
    使用 LLOneBot API 发送私聊消息到指定的 QQ 号。

    参数：
    - base_url: LLOneBot HTTP API 的基础 URL。

    - target_qq: 目标 QQ 号。

    - message: 要发送的消息内容。
    - token: (可选) 如果 LLOneBot 配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息发送成功，返回响应的 JSON 数据。
    - 如果消息发送失败，返回 None。
    """
    # 发送私聊消息的 API 端点
    send_private_msg_url = f"{base_url}/send_private_msg"
    
    # 发送消息的请求数据
    payload = {
        "user_id": target_qq,
        "message": message
    }
    
    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.post(send_private_msg_url, json=payload, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("消息发送成功！")
            return response.json()
        else:
            print("消息发送失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


#发送私聊图片
def send_private_image_msg(base_url, target_qq, image_path, summary="", token=None):
    """
    使用 LLOneBot API 发送图片消息到指定的 QQ 号。

    参数：
    - base_url: LLOneBot HTTP API 的基础 URL。

    - target_qq: 目标 QQ 号。

    - image_path: 要发送的图片路径（支持本地文件路径或URL）。
        例如 "file://D:/1.jpg" 或 "http://example.com/image.jpg"

    - summary: (可选) 图片的预览文字。

    - token: (可选) 如果 LLOneBot 配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息发送成功，返回响应的 JSON 数据。
    - 如果消息发送失败，返回 None。
    """
    # 发送私聊消息的 API 端点
    send_private_msg_url = f"{base_url}/send_private_msg"
    
    # 发送图片的请求数据
    payload = {
        "user_id": target_qq,
        "message": [
            {
                "type": "image",
                "data": {
                    "file": image_path,
                    "summary": summary
                }
            }
        ]
    }
    
    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.post(send_private_msg_url, json=payload, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("图片消息发送成功！")
            return response.json()
        else:
            print("图片消息发送失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


#发送私聊文件
def send_private_file_msg(base_url, user_id, file_path, file_name, token=None):
    """
    私聊文件消息。

    参数：
    - base_url: API 的基础 URL。

    - user_id: 目标用户的 QQ 号。

    - file_path: 文件的本地路径。
        例如 "D:/1.txt"
    - file_name: 自定义显示的文件名。
        例如 "自定义显示的文件名.txt"
    - token: (可选) 如果 Go-CQHTTP 配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息发送成功，返回响应的 JSON 数据。
    - 如果消息发送失败，返回 None。
    """
    # 发送私聊消息的 API 端点
    send_private_msg_url = f"{base_url}/send_private_msg"
    
    # 构造消息体
    message = {
        "type": "file",
        "data": {
            "file": f"file:///{file_path}",
            "name": file_name
        }
    }
    
    # 发送消息的请求数据
    payload = {
        "user_id": user_id,
        "message": message
    }
    
    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.post(send_private_msg_url, json=payload, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("私聊文件消息发送成功！")
            return response.json()
        else:
            print("私聊文件消息发送失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


#发送群消息
def send_group_msg(base_url, group_id, message, token=None):
    """
    使用 LLOneBot API 发送群消息到指定的 QQ 群。

    参数：
    - base_url: LLOneBot HTTP API 的基础 URL。
    - group_id: 目标群号。
    - message: 要发送的消息内容。
    - token: (可选) 如果 LLOneBot 配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息发送成功，返回响应的 JSON 数据。
    - 如果消息发送失败，返回 None。
    """
    send_group_msg_url = f"{base_url}/send_group_msg"
    payload = {
        "group_id": group_id,
        "message": message
    }
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.post(send_group_msg_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("群消息发送成功！")
            return response.json()
        else:
            print("群消息发送失败喵~")
            print(response.status_code, response.text)
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
    
#发送群组图片
def send_group_image_msg(base_url, group_id, image_path, summary="", token=None):
    """
    使用 LLOneBot API 发送图片消息到指定的QQ群。

    参数：
    - base_url: LLOneBot HTTP API 的基础 URL。

    - group_id: 目标群号。
        例如 123456

    - image_path: 要发送的图片路径（支持本地文件路径或URL）。
        例如 "file://D:/1.jpg" 或 "http://example.com/image.jpg"

    - summary: (可选) 图片的预览文字。

    - token: (可选) 如果 LLOneBot 配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息发送成功，返回响应的 JSON 数据。
    - 如果消息发送失败，返回 None。
    """
    # 发送群消息的 API 端点
    send_group_msg_url = f"{base_url}/send_group_msg"
    
    # 发送图片的请求数据
    payload = {
        "group_id": group_id,
        "message": [
            {
                "type": "image",
                "data": {
                    "file": image_path,
                    "summary": summary
                }
            }
        ]
    }
    
    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.post(send_group_msg_url, json=payload, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("图片消息发送成功！")
            return response.json()
        else:
            print("图片消息发送失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


#发送群文件
def send_group_file_msg(base_url, group_id, file_path, file_name, token=None):
    """
    发送群文件消息。

    参数：
    - base_url: API 的基础 URL。
    - group_id: 目标群号。
        例如 123456
    - file_path: 文件的本地路径。
        例如 "D:/1.txt"
    - file_name: 自定义显示的文件名。
        例如 "自定义显示的文件名.txt"
    - token: (可选) 如果 Go-CQHTTP 配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息发送成功，返回响应的 JSON 数据。
    - 如果消息发送失败，返回 None。
    """
    # 发送群消息的 API 端点
    send_group_msg_url = f"{base_url}/send_group_msg"
    
    # 构造消息体
    message = {
        "type": "file",
        "data": {
            "file": f"file:///{file_path}",
            "name": file_name
        }
    }
    
    # 发送消息的请求数据
    payload = {
        "group_id": group_id,
        "message": message
    }
    
    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.post(send_group_msg_url, json=payload, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("群文件消息发送成功！")
            return response.json()
        else:
            print("群文件消息发送失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None



#临时消息、私聊消息和群消息
def send_msg(base_url, message_type, target_id, message, token=None):
    """
    发送消息的方法，支持临时消息、私聊消息和群消息

    :param base_url: LLOneBot API 的基础 URL
    :param message_type: 消息类型 ('private' 或 'group')
    :param target_id: 目标 QQ 号（私聊消息）或群号（群消息）
    :param message: 要发送的消息内容
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # 根据消息类型构造请求 URL 和数据
    if message_type == 'private':
        url = f"{base_url}/send_private_msg"
        payload = {"user_id": target_id, "message": message}
    elif message_type == 'group':
        url = f"{base_url}/send_group_msg"
        payload = {"group_id": target_id, "message": message}
    else:
        print("不支持的消息类型")
        return None

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            # print("消息发送成功！")
            return response.json()
        else:
            logger.error("消息发送失败，状态码:", response.status_code)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP 请求错误: {http_err}")
        return None
    except Exception as err:
        logger.error(f"消息发送失败，其他错误: {err}")
        return None


#给用户点赞 支持群友
def send_like(base_url, user_id, times, token=None):
    """
    发送点赞表情

    :param base_url: OneBot API 的基础 URL
    :param user_id: 要发送点赞的用户的 ID
    :param times: 要发送点赞的次数
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/send_like"
    payload = {"user_id": user_id, "times": times}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("点赞成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#转发消息到好友
def forward_friend_single_msg(base_url, user_id, message_id, token=None):
    """
    转发单条消息到好友。

    参数：
    - base_url: API 的基础 URL。
    - user_id: 目标好友的 QQ 号。
    - message_id: 要转发的消息 ID。
    - token: 如果配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息转发成功，返回响应的 JSON 数据。
    - 如果消息转发失败，返回 None。
    """
    # 转发单条消息到好友的 API 端点
    url = f"{base_url}/forward_friend_single_msg"
    
    # 请求数据
    payload = {
        "user_id": user_id,
        "message_id": message_id
    }
    
    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.post(url, json=payload, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("消息成功转发给好友！")
            return response.json()
        else:
            print("转发消息到好友失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
    

#转发消息到群组
def forward_group_single_msg(base_url, group_id, message_id, token=None):
    """
    转发单条消息到群。

    参数：
    - base_url: API 的基础 URL。
    - group_id: 目标群的群号。
    - message_id: 要转发的消息 ID。
    - token: 如果配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果消息转发成功，返回响应的 JSON 数据。
    - 如果消息转发失败，返回 None。
    """
    # 转发单条消息到群的 API 端点
    url = f"{base_url}/forward_group_single_msg"
    
    # 请求数据
    payload = {
        "group_id": group_id,
        "message_id": message_id
    }
    
    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.post(url, json=payload, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("消息成功转发到群！")
            return response.json()
        else:
            print("转发消息到群失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
