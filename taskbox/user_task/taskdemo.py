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
        return f'conf1: 191******xxx signed, Run success!'

    def get_conf_list(self):
        '''这是这个任务需要的配置说明。

        这个说明会显示在任务详情页。还可以写上推荐的定时周期语法等任何你想提醒使用者的话。
        把需要配置的关键字作为列表返回。并在这里加以说明。推荐配置为简单字符串或者
        configkey1 是账号，configkey2 是密码。
        '''
        return ['configkey1', 'configkey2']



Task_demo.register()
