import requests

def can_send_image(base_url, token=None):
    """
    检查当前 OneBot 实例是否支持发送图片消息

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回是否支持发送图片消息的布尔值
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/can_send_image"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                support = data.get("data", {}).get("can_send_image", False)
                print(f"支持发送图片消息: {support}")
                return support
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return False


def can_send_record(base_url, token=None):
    """
    检查当前 OneBot 实例是否支持发送语音消息

    :param base_url: OneBot API 的基础 URL
    :param token: 身份验证 token，如果不需要可以设置为 None
    :return: 返回是否支持发送语音消息的布尔值
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    url = f"{base_url}/can_send_record"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                support = data.get("data", {}).get("can_send_record", False)
                print(f"支持发送语音消息: {support}")
                return support
            else:
                print("API 返回错误:", data.get("msg"))
        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求过程中发生错误:", e)

    return False
