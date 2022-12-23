---
layout: default
---

[常见问题](./qa)💡 | [更新日志](./release_note)✨ | [如何贡献](./contribute)💪 | [任务市场](./taskmarket)🍻

任务盒子（TaskBox，以下简称盒子）是一个**运行在 Serverless 平台的个人定时任务框架**。它注重稳定、性能和扩展性。基于 AWS Lambda + [DynamoDB][2] + S3 + APIGW + EventBridge scheduler 编写。


## 1 主要特性

- 全免费，利用 AWS 给开发者的[永久免费额度](https://aws.amazon.com/cn/free/) 🎉
- 简单部署。基于 AWS SAM 应用模板，能自动的绝不手动。
- Web 任务列表。支持任务增删改查，可绑定个人域名。
- 简单的登录鉴权功能，并利用 AWS Api-Gateway 做了**访问安全限制**，狠狠防住暴力破解！
- 配置、任务周期可在网页设置（不同任务支持自定义配置），任务cookie过期1秒钟更换！
- 注重性能。无 web 框架（flask/bottle等），无冗余代码。并得益于 AWS 函数计算和数据库的高可用、高性能，网页冷启动时间 1s 内，后续网页请求基本在 5ms 内完成。<small>不包含DynamoDB查询时延 10ms 以内</small>
- 提供了网页版的 Shell 和 Python 命令接口，临时使用不在话下。
- 极具扩展性。任务插件化，根据[贡献指南](./contribute)一分钟创建属于你的任务。还可在[任务市场](./taskmarket)寻找~~丰富扩展~~求PR
- ...

![index](/static/img/box_index.png)
![exc page](/static/img/box_exc.png)

## 2 开始使用

1、Fork 本仓库，并在你仓库的 setting -> Actions secrets 设置如下三个变量
```
AWS_ACCESS_KEY_ID 
AWS_SECRET_ACCESS_KEY
WEB_PASSWORD
```
前两个变量从你的 aws 账户获取，一般在[这里设置][1]，第三个是用来登录盒子的密码，现在鉴权方式比较简陋，所以推荐设置一个**强密码**。

2、推送一个 commit 到 master 分支触发自动部署到 AWS  
从 AWS api-gateway控制台能够找到访问的api。并且可以自定义域名。

TODO 一些权限问题导致的失败处理方式。


[1]: https://us-east-1.console.aws.amazon.com/iam/home#/security_credentials$access_key
[2]: https://docs.amazonaws.cn/amazondynamodb/latest/developerguide/Introduction.html 'DynamoDB介绍'

