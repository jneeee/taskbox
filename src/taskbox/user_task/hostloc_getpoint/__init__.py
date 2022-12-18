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
