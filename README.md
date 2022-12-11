## TaskDb(Task Dashboard) 任务仪表板

我是图

TaskDB(Task Dashboard) 是一个个人定时任务框架。它注重稳定和性能。基于 AWS Lambda + DynamoDB + S3 + APIGW + EventBridge scheduler 的高可用 Serverless 应用平台编写。主要特点如下：

- 全免费，利用 AWS 给开发者的永久[免费额度](https://aws.amazon.com/cn/free/) 🎉
- 定制的 web 网页，任务列表。支持任务增删改查，可绑定个人域名。
- 注重性能。没用 web 框架（flask/bottle等），无冗余代码。并得益于 AWS 函数计算和数据库的高可用、高性能，服务冷启动时间 0.5s 内，后续网页请求基本在 0.001s 内完成。
- 简单的登录鉴权功能
- 提供了网页版的 Shell 和 Python 命令接口。
- 任务插件化。只要简单继承 taskdb.task.Task 类，实现一个 step 方法，就是一个属于你自己的定时任务。
- 安全。API-GW 配置了访问限额，（TODO）应用内实现黑名单机制。
- 简单上手。基于 AWS SAM 应用模板，能自动的绝不手动。

我是图

快速更新中，欢迎 PR

### TODO
- task.config = [{}, ] 实现多账号，~~你可以跟你朋友炫技了~~。
- 应用内实现黑名单机制。IP 黑名单加到 ApiGW

