---
layout: default
---

任务盒子（TaskBox，以下简称盒子）是一个运行在 Serverless 平台的个人定时任务框架。它注重稳定、性能和扩展性。基于 AWS Lambda + DynamoDB + S3 + APIGW + EventBridge scheduler 编写。

两张截图

## 1 特性

- 全免费，利用 AWS 给开发者的[永久免费额度](https://aws.amazon.com/cn/free/) 🎉
- 简单部署。基于 AWS SAM 应用模板，能自动的绝不手动。
- 定制的 web 网页，任务列表。支持任务增删改查，可绑定个人域名，向朋友秀出你的个人助手。
- 简单的登录鉴权功能，并利用 AWS Api-Gateway 做了**访问安全限制**，狠狠防住暴力破解。
- 注重性能。无 web 框架（flask/bottle），无冗余代码。并得益于 AWS 函数计算和数据库的高可用、高性能，网页冷启动时间 0.5s 内，后续网页请求基本在 0.001s 内完成。<small>不包含DynamoDB查询时延 10ms 左右</small>
- 提供了网页版的 Shell 和 Python 命令接口，临时使用不在话下。
- 任务插件化。根据[贡献指南](./contribute)一分钟创建属于你的任务。还可在[任务市场]寻找~~丰富扩展~~求PR

更多特性请查看[更新日志](./release_note)

## 2 开始使用

## 3 如何贡献
参考 [贡献指南](./contribute)
一点呼吁：本着开源、共享精神，希望大家写出有意义的、不浪费算力（免费额度40wGBs/月）的任务，让这件事情、这个项目可持续发展。

## 4 问题和求助

