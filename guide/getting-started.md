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
   cd DreamSu
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
    "base_url": "http://localhost:3001",  /* 这里是你的 OneBot服务端 的 HTTP 服务监听地址与端口 */
    "rtmsg_prot": 18080,  /* 这里是你的 OneBot服务端 的 HTTP 事件上报的监听端口 */
    "token": None,  /* 这里是你的 OneBot服务端 的 Access token ， 默认为空 ，字符串记得带引号 */
    "masters": [  /* 这里是主人的号码 ，支持多个号码 */
        1234567890, 
        9876543210
    ],
    "log_level": "debug"  /* 日志等级 ，info 或 debug */
}
```

！！请注意，json中不支持注释，请不要直接复制上述内容。\
截至目前暂未适配ws连接

## 使用方法

提供关于如何运行和使用项目的简单说明。

```bash
python main.py
```

根据需要提供更多的使用例子或命令。