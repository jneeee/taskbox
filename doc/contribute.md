---
layout: default
title: 如何贡献 - 任务盒子
---

任务盒子是个开源项目，目前暂时仅我在工作之余维护着。如果你发现项目的 Bug 或者想要贡献一个任务，欢迎提交 Pull request.


## 1分钟创建你自己的任务

只要简单继承 taskbox.taskbase.Task 类，实现一个 step 方法，就是一个属于你自己的定时任务。

```python
# taskbox/user_task/taskdemo.py
from taskbox.taskbase.task import Task


__all__ = ['Task_demo']


class Task_demo(Task):
    '''任务介绍

    这里是任务介绍，会显示在任务详情页。
    '''
    name_zh = '任务的中文名，网页展示用'

    def __init__(self, *args, **kwargs):
        # 这是任务初始化的地方，由盒子完成，保持不变即可
        super().__init__(*args, **kwargs)

    def step(self, config):
        '''这里是任务具体做的事情

        盒子会根据设置的周期，调用这个方法。返回的结果会显示在web的‘结果’一栏。
        注意不要回显敏感的配置信息！
        '''
        conf1 = config.get('configkey1')
        return f'conf1: 191******xxx signed, Run success!'

    def get_conf_list(self):
        '''这是这个任务需要的配置说明。

        这个说明会显示在任务详情页。还可以写上推荐的定时周期语法等任何你想提醒使用者的话。
        把需要配置的关键字作为列表返回。并在这里加以说明。推荐配置为简单字符串或者json
        '''
        return {
            'configkey1': '这里是配置说明，会显示在网页',
            'configkey2': '这里是配置说明，会显示在网页',
        }

# 向盒子注册这个Task，必要的，不然找不到任务。
Task_demo.register()

# requirements.txt

```

当前运行环境是 Python3.9
触发 AWS CI 之后，盒子会自动查找目录下所有的 requirements.txt 并安装依赖。（TODO 可能要更改 template.yml 层定义以触发创建新的 layer）

## 使用 submodule 贡献任务

如果你希望把任务贡献给任务盒子，可以创建一个你自己的 git 仓库，并把它添加到 taskbox 的 submodule 里面（创建一个pull requests）
下面以论坛获取积分的程序为例，适配盒子。


