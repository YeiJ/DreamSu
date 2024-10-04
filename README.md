<p align="center">
  <a href="https://github.com/YeiJ/DreamSu">
    <img src="images/DreamSu.png" width="200" height="200" alt="DreamSu">
  </a>
</p>

<div align="center">

# DreamSu

_✨ 基于 OneBotv11 上游接口机器人Api的 Python 原生实现 ✨_  


</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/YeiJ/DreamSu/main/LICENSE">
    <img src="https://img.shields.io/github/license/YeiJ/DreamSu" alt="license">
  </a>
  <a href="https://github.com/howmanybots/onebot/blob/master/README.md">
    <img src="https://img.shields.io/badge/OneBot-v11-blue?style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="gensokyo">
  </a>
  
</p>




## 介绍

一个通过 OneBotv11 协议的 HTTP 监听端口实现的 Python 机器人插件管理器框架。\
DreamSu 意为苏梦，我的很多项目都叫这个名字。

## 目录

- [项目背景](#项目背景)
- [接口](#接口)
- [安装](#安装) 
- [喵](#喵)
- [插件开发指南](./doc/插件开发文档.md)
- [近期计划](#近期计划)
- [许可证](#许可证)

## 项目背景

喵~ ~~第一次写Python项目，就开了个项目练手，可能比较臃肿，欢迎提建议。~~

## 接口

目前已实现
- [x] HTTP API
- [x] 正向 WebSocket

以下接口将会逐步适配，但不是现在 ~~（写不会了~~
- [x] 反向 HTTP POST
- [x] 反向 WebSocket

## 安装

[部署向导](./guide/getting-started.md)

注：目前该项目仅在 Windows 下进行了测试，不能保证能在 Linux 下完美运行。如有 bug 请立即反馈，谢谢 :)

## 喵

本项目纯写着玩，有兴趣可以在遵循许可证的前提下拿去玩。有bug发现或者新的功能提议可以提issue。

## 近期计划

1. 正在计划开发本项目的web后台，用于方便管理配置文件。
2. 计划编写插件的配置文件接口的文件规范，用以便于web后台自动生成第三方插件的配置文件的操作界面。

## 许可证

本项目使用 GPL-3.0 许可证 - 参见 [LICENSE](LICENSE) 文件了解更多详情。

本项目仅在Github上发布仓库，[项目地址](https://github.com/YeiJ/DreamSu)。若在其他git仓库见到本项目军不是本人发布，使用时请注意甄别。