---
layout: default
title: 任务市场
---


市场里面的任务会经过检查，确保各位隐私，杜绝后门！
但限于个人能力、精力有限，需要提醒你的账号密码有可能会暴露给任务提供者。当前任务页会说明可信任的任务的 commit-id ，在这个id 之后的版本的任务安全性，以及自行管理的其他 submodule 任务，盒子不做数据安全保证，请仔细甄别！！！

todo 变量控制导入的module

### 添加方式

hostloc_getpoint 已默认添加，此处仅做演示。
```
git submodule add https://github.com/jneeee/hostloc_getPoints.git \
    src/taskbox/user_task/hostloc_getpoint
```

不配置定时器不会触发任务。如果你想删掉不需要的任务，用git submodule deinit <path> (TODO)

### 如何贡献？
参考[贡献指南](/taskbox/contribute)贡献任务


## 任务列表

* 天翼云盘签到: 已内置
* 定时访问：已内置
* [jneeee/hostloc_getPoints](https://github.com/jneeee/hostloc_getPoints) 获取hostloc论坛积分
TODO
