# 部署向导

## 目录

- [安装](#安装)
- [依赖](#依赖)
- [配置文件](#配置文件)
- [使用方法](#使用方法)

## 安装

Python 版本建议在 3.9 及以上

请按照以下步骤进行安装：

1. 克隆项目仓库：

   ```bash
   git clone https://github.com/YeiJ/DreamSu.git
   cd DreamSu_LLOBPM
   ```

2. 创建并激活虚拟环境（可选，但推荐）：

   - **Windows:**

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - **macOS 和 Linux:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

## 依赖

项目所需的所有依赖都列在 `requirements.txt` 文件中。你可以使用以下命令安装这些依赖：

```bash
pip install -r requirements.txt
```

## 配置文件

需要将项目的配置文件 `config\config.json` 中的相关数据替换为你自己的：

```json
{
    "rtmsg_type": "ws", 
    /* 这里是消息获取方式 , 填 http 或 ws , 分别使用 rt_http_prot 或 f_ws_url */

    "rq_http_url": "http://localhost:3001",  /* ### 必填项 ### */
    /* 这里是你的 OneBot 服务端 的 HTTP 服务监听地址与端口 */
    "rt_http_prot": 18080,  
    /* 这里是你的 OneBot 服务端 接收 HTTP 事件上报的监听端口 */

    "f_ws_url": "ws://localhost:3002",  
    /* 这里是你的 OneBot 服务端的正向 ws 连接地址与端口 */

    "token": "",  
    /* 这里是你的 OneBot服务端 的 Access token ， 默认为空 ，字符串记得带引号 */
    "masters": [  
        /* 这里是主人的号码 ，支持多个号码 */
        1234567890, 
        9876543210
    ],
    "log_level": "info"  
    /* 日志等级 , info 或 debug */
}
```

截至目前暂未适配反向 ws 连接

## 使用方法

提供关于如何运行和使用项目的简单说明。

```bash
python main.py
```

根据需要提供更多的使用例子或命令。

本项目提供了几个示例插件用于测试和参考，以下是列表：

`p_echo.py` （私聊自动复读） 、\
`p_status.py` （查询系统状态<仅主人账号关键词触发>） 、\
\
`p_keywordreply` （关键词自动回复，支持设置单词条群聊私聊黑白名单） 、\
`p_wordsRSent` （随机发送指定词库文件词条<可设置词条个数>到指定群聊或私聊，可设置定时触发或关键词触发）