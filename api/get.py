import requests
import logging

logger = logging.getLogger("api.get")

def get_msg(base_url, message_id, token=None):
    """
    获取指定消息的详细信息

    :param base_url: OneBot API 的基础 URL
    :param message_id: 要获取的消息的 ID
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    url = f"{base_url}/get_msg"
    payload = {"message_id": message_id}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                return data.get("data")
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_forward_msg(base_url, message_id, token=None):
    """
    获取合并转发消息的详细内容

    :param base_url: OneBot API 的基础 URL
    :param message_id: 要获取的合并转发消息的 ID
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_forward_msg"
    payload = {"message_id": message_id}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                return data.get("data")
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_login_info(base_url, token=None):
    # 设置请求头
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # 构造请求 URL
    url = f"{base_url}/get_login_info"

    try:
        # 发送 HTTP POST 请求
        response = requests.post(url, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                return data.get("data")
            else:
                print("API返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_stranger_info(base_url, user_id, no_cache=False, token=None):
    """
    获取陌生人（非好友）的详细信息

    :param base_url: OneBot API 的基础 URL
    :param user_id: 要获取信息的用户的 QQ 号
    :param no_cache: 是否不使用缓存，默认为 False
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_stranger_info"
    params = {
        "user_id": user_id,
        "no_cache": no_cache
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("获取陌生人信息成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_group_info(base_url, group_id, no_cache=False, token=None):
    """
    获取群信息

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param no_cache: 是否不使用缓存，默认为 False
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_group_info"
    params = {
        "group_id": group_id,
        "no_cache": no_cache
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                logger.debug("获取群信息成功")
                print("\n")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_group_member_info(base_url, group_id, user_id, no_cache=False, token=None):
    """
    获取群成员信息

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param user_id: 成员的 QQ 号
    :param no_cache: 是否不使用缓存，默认为 False
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_group_member_info"
    params = {
        "group_id": group_id,
        "user_id": user_id,
        "no_cache": no_cache
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                logger.debug("获取群成员信息成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_friend_list(base_url, token=None):
    """
    获取好友列表

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_friend_list"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                logger.debug("获取好友列表成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_group_ignore_add_request(base_url, token=None):
    """
    获取过滤后的入群请求。

    参数：
    - base_url: API 的基础 URL。
    - token: 如果配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果请求成功，返回响应的 JSON 数据。
    - 如果请求失败，返回 None。
    """
    # 获取过滤后的入群请求的 API 端点
    url = f"{base_url}/get_group_ignore_add_request"

    # 设置请求头，如果需要 token 授权
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # 发送请求
        response = requests.get(url, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("成功获取过滤后的入群请求！")
            return response.json()
        else:
            print("获取过滤后的入群请求失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


def get_group_list(base_url, token=None):
    """
    获取群列表

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_group_list"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                logger.debug("获取群列表成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None

def get_group_member_list(base_url, group_id, token=None):
    """
    获取指定群的所有成员信息列表

    :param base_url: OneBot API 的基础 URL
    :param group_id: 群号
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_group_member_list"
    params = {
        "group_id": group_id
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("获取群成员列表成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_file(base_url, file_id, token=None):
    """
    下载群文件或私聊文件。

    参数：
    - base_url: API 的基础 URL。
    - file_id: 文件 ID，指示要下载的文件。
        例如 "/xxxxx-xxxxx"
    - token: 如果配置了鉴权 Token，需要提供该 Token。

    返回值：
    - 如果请求成功，返回响应的二进制文件数据。
    - 如果请求失败，返回 None。
    """
    # 下载文件的 API 端点
    url = f"{base_url}/get_file"
    
    # 请求数据
    payload = {
        "file_id": file_id
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
            print("文件下载成功！")
            return response.content  # 返回文件的二进制数据
        else:
            print("文件下载失败喵~")
            print(response.status_code, response.text)
            return None

    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


###########
#
#

def get_cookies(base_url, domain=None, token=None):
    """
    获取当前 OneBot 实例的 Cookie 信息

    :param base_url: OneBot API 的基础 URL
    :param domain: 可选参数，指定需要的 Cookie 的域
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {"domain": domain} if domain else {}

    url = f"{base_url}/get_cookies"

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("获取 Cookie 成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_csrf_token(base_url, token=None):
    """
    获取当前 OneBot 实例的 CSRF Token

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_csrf_token"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("获取 CSRF Token 成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_credentials(base_url, token=None):
    """
    获取当前 OneBot 实例的凭据信息

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_credentials"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("获取凭据信息成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None

#
#
###########


def get_record(base_url, file, out_format='mp3', token=None):
    """
    获取语音文件

    :param base_url: OneBot API 的基础 URL
    :param file: 文件名，例如通过消息接收到的语音文件名
    :param out_format: 输出的文件格式，默认为 'mp3'
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {"file": file, "out_format": out_format}

    url = f"{base_url}/get_record"

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            print("获取语音文件成功")
            return response.content  # 返回语音文件的二进制数据
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_image(base_url, file, token=None):
    """
    获取图片文件

    :param base_url: OneBot API 的基础 URL
    :param file: 文件名，例如通过消息接收到的图片文件名
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {"file": file}

    url = f"{base_url}/get_image"

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            print("获取图片文件成功")
            return response.content  # 返回图片文件的二进制数据
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


##############


def get_status(base_url, token=None):
    """
    获取当前 OneBot 实例的运行状态

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_status"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("获取运行状态成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


def get_version_info(base_url, token=None):
    """
    获取当前 OneBot 实例的版本信息

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/get_version_info"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("获取版本信息成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None


