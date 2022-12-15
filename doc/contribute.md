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
    '''这里写这个任务的说明，会显示在任务详情页

    它是干嘛的。类名就是
    '''
    name_zh = '任务的中文名，网页展示用'

    def __init__(self, *args, **kwargs):
        # 这是任务初始化的地方，由盒子完成，保持不变即可
        super().__init__(*args, **kwargs)

    def step(self, config):
        '''实现我

        输入是一个配置字典，key是 get_conf_list 的返回中定义的。
        这里是任务具体要做的事情
        '''
        conf1 = config.get('configkey1')
        return f'conf1: {conf1}, Run success!'

    def get_conf_list(self):
        '''Config for task Demo_task

        这里是执行任务需要的配置的说明，会显示在web任务详情页
        :configkey1: key1 的描述
        :configkey2: key2 的描述
        还可以提一下推荐的定时任务周期和理由。会被使用者看见
        '''
        return ['configkey1', 'configkey2']

# 向盒子注册这个Task，必要的，不然找不到。别重写 register 函数
Task_demo.register()

# requirements.txt

```

当前运行环境是 Python3.9
触发 AWS CI 之后，盒子会自动查找目录下所有的 requirements.txt 并安装依赖。（TODO 可能要更改 template.yml 层定义以触发创建新的 layer）

## 使用 submodule 贡献任务

如果你希望把任务贡献给任务盒子，可以创建一个你自己的 git 仓库，并把它添加到 taskbox 的 submodule 里面（创建一个pull requests）
下面以论坛获取积分的程序为例，适配盒子。


