---
layout: default
title: 如何贡献 - 任务盒子
---

任务盒子是个开源项目，目前暂时仅我在工作之余维护着。如果你发现项目的 Bug 或者想要**贡献一个任务**，欢迎提交 Pull request 到 [TaskBox](https://github.com/jneeee/taskbox)。

下面介绍两种贡献任务的方法。第一种是最简单的创建自己的 Task 方法，适合比较个人的，不公开的任务，在你的私有仓库里管理就行。第二种是将现有脚本适配到盒子，通过创建/fork一个现有的脚本库，集成到盒子里。

## 1分钟创建你自己的任务

只要简单继承 taskbox.taskbase.task.Task 类，实现一个 step 方法，就创建了一个属于你自己的定时任务。

```python
# taskbox/user_task/taskdemo.py
from taskbox.taskbase.task import Task
from taskbox.utils.tools import LOG


__all__ = ['Task_demo']

class Task_demo(Task):
    '''任务介绍

    这里是任务介绍，会显示在任务详情页。
    '''
    name_zh = '测试任务'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def step(self, config):
        '''这里是任务具体做的事情

        盒子会根据设置的周期，调用这个方法。返回的结果会显示在web的‘结果’一栏。
        '''
        conf1 = config.get('configkey1')
        return 'conf1: 191******xxx signed, Run success!'

    def get_conf_list(self):
        '''这是这个任务需要的配置说明。

        这个说明会显示在任务详情页。还可以写上推荐的定时周期语法等任何你想提醒使用者的话。
        把需要配置的关键字作为列表返回。并在这里加以说明。推荐配置为简单字符串或者json。
        '''
        return {
            'configkey1': '这里是配置说明，会显示在网页',
            'configkey2': '这里是配置说明，会显示在网页',
        }


Task_demo.register()
```

之后需要把它加到版本控制，推到你的 github 私有仓库触发CI。
```
(py39) jn@honer:~/taskbox$ git add src/taskbox/user_task/taskdemo.py
(py39) jn@honer:~/taskbox$ git commit -m 'add my own task'
(py39) jn@honer:~/taskbox$ git push aws HEAD:master
```

<hr>

## 使用 submodule 贡献任务

如果你希望把任务贡献给任务盒子，可以创建一个你自己的 git 仓库，并把它添加到 taskbox 的 submodule 里面（创建一个pull requests）
下面以论坛获取积分的程序为例，适配盒子。

**第一步 准备工作**
先找到原仓库 [Jox2018/hostloc_getPoints](https://github.com/Jox2018/hostloc_getPoints) fork 一份。

**第二步 添加子模块**
命令如下。Git 会把 hostloc_getPoints 仓库代码克隆到 `taskbox/user_task/hostloc_getpoint` 下面。
```shell
(py39) jn@honer:~/taskbox$ git submodule add https://github.com/jneeee/hostloc_getPoints.git src/taskbox/user_task/hostloc_getpoint
```

**第三步 适配盒子**

修改原来的执行内容，并继承 taskbox.taskbase.task.Task ，这一步类似第一种任务，就是把原来脚本的主进程挪到 step() 函数下面，在接受一个原来配在环境变量里的账户密码。这样盒子就能控制脚本的执行了。部分代码如下，具体的可以看看 [Commit: adapt taskbox][1]

```python
# 新文件 src/taskbox/user_task/hostloc_getpoint/__init__.py
from taskbox.taskbase.task import Task
from taskbox.utils.tools import LOG

from .hostloc_auto_get_points import run_getpoint


__all__ = ['hostloc_getpoint']

class hostloc_getpoint(Task):
    '''获取hostloc积分的任务
    '''
    name_zh = '获取hostloc积分'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def step(self, config):
        '''这里是任务具体做的事情

        盒子会根据设置的周期，调用这个方法。返回的结果会显示在web的‘结果’一栏。
        '''
        account = config.get('account')
        password = config.get('password')
        return run_getpoint(account, password)

    def get_conf_list(self):
        '''获取积分的配置说明

        盒子本身和这个任务都支持多账号，因此两种设置方法都可以。
        '''
        return {
            'account': "账户名，多账号以英文逗号','分割",
            'password': "密码，以英文逗号','分割，要和账户数量相同个数",
        }

hostloc_getpoint.register()

# 原脚本中的主程序 src/taskbox/user_task/hostloc_getpoint/hostloc_auto_get_points.py
def run_getpoint(username, password):
    user_list = username.split(",")
    passwd_list = password.split(",")

    res = []
    if len(user_list) != len(passwd_list):
        res.append("用户名与密码个数不匹配，请检查环境变量设置是否错漏！")
    else:
        print_my_ip()
        res.append("共检测到", len(user_list), "个帐户，开始获取积分")
        res.append("*" * 30)

        # 依次登录帐户获取积分，出现错误时不中断程序继续尝试下一个帐户
        for i in range(len(user_list)):
            try:
                s = login(user_list[i], passwd_list[i])
                get_points(s, i + 1)
                res.append("*" * 30)
            except Exception as e:
                res.append("程序执行异常：" + str(e))
                res.append("*" * 30)
            continue

        res.append("程序执行完毕，获取积分过程结束")
    return res
```

当前运行环境是 Python3.9，触发 AWS CI 之后，盒子会自动查找目录下所有的 requirements.txt 并安装依赖。由于原脚本依赖的 `pyaes` 还没加到依赖。需要添加一个新的依赖文件 taskbox/user_task/hostloc_getpoint/requirements.txt
```
# src/taskbox/user_task/hostloc_getpoint/requirements.txt
pyaes
```

> 提醒：如果是第一次部署，新加的依赖文件会自动添加成功。如果是后面推新的版本/任务，还要修改 template.yml 里面的 libs -> Properties -> Description 来触发层的更新。

**第四步 推送修改**

这里要推送3个地方，第一个是你fork的仓库，这是其他人找到你修改的地方。第二个是 TaskBox 开源库，让别人看到你贡献的任务。第三个是 AWS 为你创建的私有仓库，部署到 AWS 用的。

```shell
(py39) jn@honer:~/taskbox$ cd src/taskbox/user_task/hostloc_getpoint
(py39) jn@honer:~/taskbox/src/taskbox/user_task/hostloc_getpoint$ git add .
(py39) jn@honer:~/taskbox/src/taskbox/user_task/hostloc_getpoint$ git commit -m 'adapt TaskBox'
(py39) jn@honer:~/taskbox/src/taskbox/user_task/hostloc_getpoint$ git push
(py39) jn@honer:~/taskbox/src/taskbox/user_task/hostloc_getpoint$ cd -
(py39) jn@honer:~/taskbox$ git add src/taskbox/user_task/hostloc_getpoint .gitmodules
# 检查一下远端分支名称
(py39) jn@honer:~/taskbox$ git remote -v
aws     git@github.com:<Your id>/mytaskbox.git (fetch) <--- 私有仓库，部署到 AWS 用
aws     git@github.com:<Your id>/mytaskbox.git (push)
origin  git@github.com:<Your id>/taskbox.git (fetch) <--- 你fork的TaskBox开源库，提交 Pull requests 用
origin  git@github.com:<Your id>/taskbox.git (push)
(py39) jn@honer:~/taskbox$ git push aws HEAD:master
(py39) jn@honer:~/taskbox$ git push origin HEAD:master
# 再去 TaskBox 网页提交 Pull 即可。
```

（完）

[1]: https://github.com/jneeee/hostloc_getPoints/commit/f8151984ab42ec275f8012008d4bbcc58d582b09 'adapt taskbox'
