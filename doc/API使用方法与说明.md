### API 的使用方法

- 所有 API 接口实现都在 `api/` 下，均符合OneBotv11标准。
- 本框架内置了一些额外的方法方便插件编写，方法实现在 `api/bot` 下，不用导入库，可直接通过 bot 实例调用。

---

### 手动导入本框架实现的 OneBotv11 相关 API 库

在插件文件中可手动导入 OBv11 的库进行使用，例：

```python
from api.send import send_private_msg

send_private_msg(self.bot.base_url, user_id, massage, self.bot.token)
```

此文件夹中提供了本框架支持的几乎所有OB的HTTP监听API的单文件调用示例，可参考使用。

### 使用本框架内置的额外方法

详见 `更多方法/` 下的其他 md 文件

---

### 文件类 API 说明

图片上传和文件上传 API 所传递的 文件路径 `file_path` 必须是 OneBot 所运行设备的路径，跨设备使用本 DreamSuOB 框架和 OneBot 时请注意此项。

### 注

 - 转发方法 `forward_friend_single_msg` 和 `forward_group_single_msg ` 放在了 `api.send` （也就是 `api\send.py` 文件）中

 ---
 ---

 ### 附录

 - 目前支持的 OneBotv11 API 列表

    `can_send_image(base_url, token=token)`\
    `can_send_record(base_url, token=token)`\
    \
    `clean_cache(base_url, token=token)`\
    \
    `delete_msg(base_url, message_id, token)`\
    \
    `forward_friend_single_msg(base_url, user_id, message_id, token)`\
    `forward_group_single_msg(base_url, user_id, group_id, token)`\
    \
    `get_cookies(base_url, domain=domain, token=token)`\
    `get_credentials(base_url, token=token)`\
    `get_csrf_token(base_url, token=token)`\
    `get_file(base_url, file_id, token=token)`\
    `get_forward_msg(base_url, message_id, token)`\
    `get_friend_list(base_url, token=token)`\
    `get_group_ignore_add_request(base_url, token=token)`\
    `get_group_info(base_url, group_id, no_cache=False, token=token)`\
    `get_group_list(base_url, token=token)`\
    `get_group_member_info(base_url, group_id, user_id, no_cache=False, token=token)`\
    `get_group_member_list(base_url, group_id, token=token)`\
    `get_image(base_url, file, token=token)`\
    `get_login_info(base_url, token)`\
    `get_msg(base_url, message_id, token)`\
    `get_record(base_url, file, out_format='amr', token=token)`\
    `get_status(base_url, token=token)`\
    `get_stranger_info(base_url, user_id, no_cache, token=token)`\
    `get_version_info(base_url, token=token)`\
    \
    `send_group_file_msg(base_url, group_id, file_path, file_name, token=token)`\
    `send_group_image_msg(base_url, group_id, image_path, summary, token)`\
    `send_group_msg(base_url, group_id, message, token)`\
    `send_like(base_url, user_id, times, token)`\
    `send_msg(base_url, message_type, target_id, message, token)`\
    `send_private_file_msg(base_url, user_id, file_path, file_name, token=token)`\
    `send_private_image_msg(base_url, target_qq, image_path, summary, token)`\
    `send_private_msg(base_url, target_qq, message, token)`\
    \
    `set_friend_add_request(base_url, flag, approve, remark, token=token)`\
    `set_group_add_request(base_url, flag, sub_type, approve, reason, token=token)`\
    `set_group_admin(base_url, group_id, user_id, enable, token=token)`\
    `set_group_ban(base_url, group_id, user_id, duration, token=token)`\
    `set_group_card(base_url, group_id, user_id, card, token=token)`\
    `set_group_kick(base_url, group_id, user_id, reject_add_request, token=token)`\
    `set_group_leave(base_url, group_id, is_dismiss=False, token=token)`\
    `set_group_name(base_url, group_id, group_name, token=token)`\
    `set_group_special_title(base_url, group_id, user_id, special_title, token=token)`\
    `set_group_whole_ban(base_url, group_id, enable, token)`\
    `set_restart(base_url, token=token)`\