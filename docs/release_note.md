---
layout: default
title: 更新日志
description: 任务盒子的更新日志
---

## Todo
* 插件（任务）市场
* 完善文档
* 对不在Task列表里的任务，从数据库里删除
* email 订阅功能
* 数据在响应后再写到db

### v2.2 onging
* task 日志查询，单次执行的所有日志，最多30天。

### v2.1
* 用 cookie 管理登录会话，用装饰器管理登录鉴权的网页

### v2.0 (2022.12.20)

TaskBox 开源

* 创建 Eventbridge scheduler 绑定到任务
* 任务的启停功能
* 同一任务多账号配置
* 任务详情页可修改配置

### v1.0 (2022.12.11)

* 增加任务列表，任务详情页
* 登录功能, web 回显操作结果消息。
* 网页增删改查 Dynamodb
* 网页增加 Shell 和 Python 执行接口
* 可扩展的任务对象
