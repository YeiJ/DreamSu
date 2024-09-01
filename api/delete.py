import requests

def delete_msg(base_url, message_id, token=None):
    """
    撤回指定的消息

    :param base_url: OneBot API 的基础 URL
    :param message_id: 要撤回的消息的 ID
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回的响应数据或 None
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/delete_msg"
    payload = {"message_id": message_id}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("消息撤回成功")
                return data
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return None
