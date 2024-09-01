import requests

#踢出群成员
def set_group_kick(base_url, group_id, user_id, reject_add_request=False, token=None):
    """
    将群成员移出群聊

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param user_id: 要踢出的成员的 QQ 号
    :param reject_add_request: 是否拒绝此人再次加群请求
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_kick"
    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "reject_add_request": reject_add_request
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("成员已被踢出")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#群组单人禁言
def set_group_ban(base_url, group_id, user_id, duration, token=None):
    """
    禁言群成员

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param user_id: 要禁言的成员的 QQ 号
    :param duration: 禁言时长，单位为秒
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_ban"
    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "duration": duration
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("成员已被禁言")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#全体禁言
def set_group_whole_ban(base_url, group_id, enable=True, token=None):
    """
    启用或禁用群全员禁言

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param enable: 是否启用全员禁言
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_whole_ban"
    payload = {
        "group_id": group_id,
        "enable": enable
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                if enable:
                    print("群全员禁言已启用")
                else:
                    print("群全员禁言已关闭")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#设置群管
def set_group_admin(base_url, group_id, user_id, enable=True, token=None):
    """
    设置或取消群管理员

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param user_id: 要设置/取消管理员的成员的 QQ 号
    :param enable: 是否设置为管理员
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_admin"
    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "enable": enable
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                if enable:
                    print("已设置为群管理员")
                else:
                    print("已取消群管理员")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#设置群员群名片
def set_group_card(base_url, group_id, user_id, card=None, token=None):
    """
    设置群成员的群名片

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param user_id: 要设置名片的成员的 QQ 号
    :param card: 新的群名片，若为 None 则删除群名片
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_card"
    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "card": card
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("群名片已设置")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#修改群名称
def set_group_name(base_url, group_id, group_name, token=None):
    """
    修改群名称

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param group_name: 新的群名称
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_name"
    payload = {
        "group_id": group_id,
        "group_name": group_name
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("群名称已修改")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#退出指定群聊
def set_group_leave(base_url, group_id, is_dismiss=False, token=None):
    """
    退出群聊或解散群聊

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param is_dismiss: 是否解散群聊，默认为 False（退出群聊）
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_leave"
    payload = {
        "group_id": group_id,
        "is_dismiss": is_dismiss
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("已退出群聊" if not is_dismiss else "群已解散")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#设置群成员的群头衔
def set_group_special_title(base_url, group_id, user_id, special_title=None, token=None):
    """
    设置群成员的群头衔（特别称号）

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param user_id: 要设置称号的成员的 QQ 号
    :param special_title: 特别称号，若为 None 则删除群头衔
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_special_title"
    payload = {
        "group_id": group_id,
        "user_id": user_id,
        "special_title": special_title
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("群头衔已设置")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#处理好友请求
def set_friend_add_request(base_url, flag, approve=True, remark=None, token=None):
    """
    处理加好友请求

    :param base_url: OneBot API 的基础 URL
    :param flag: 加好友请求的 flag，唯一标识
    :param approve: 是否同意该请求，默认为 True（同意）
    :param remark: 好友备注，只有在 approve 为 True 时有效
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_friend_add_request"
    payload = {
        "flag": flag,
        "approve": approve,
        "remark": remark
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("加好友请求已处理")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#处理加群请求或邀请
def set_group_add_request(base_url, flag, sub_type, approve=True, reason=None, token=None):
    """
    处理加群请求或邀请

    :param base_url: OneBot API 的基础 URL
    :param flag: 加群请求的 flag，唯一标识
    :param sub_type: 请求类型，`add` 表示加群请求，`invite` 表示邀请入群请求
    :param approve: 是否同意该请求，默认为 True（同意）
    :param reason: 拒绝理由，仅在 approve 为 False 时有效
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_group_add_request"
    payload = {
        "flag": flag,
        "sub_type": sub_type,
        "approve": approve,
        "reason": reason
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("加群请求或邀请已处理")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#########
#重启 OneBot 实例
def set_restart(base_url, token=None):
    """
    重启 OneBot 实例

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/set_restart"

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("重启命令已发送")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


#清理实例缓存
def clean_cache(base_url, token=None):
    """
    清理 OneBot 实例的缓存数据

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/clean_cache"

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("缓存已清理")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None
