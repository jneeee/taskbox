import requests

from taskbox.taskbase.task import Task
from taskbox.utils.tools import LOG


__all__ = ['CornReq']

class CornReq(Task):
    '''定时访问一个网址，万金油任务，后续加入自定义 data/param
    '''
    name_zh = '定时访问'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def step(self, config):
        '''这里是任务具体做的事情

        盒子会根据设置的周期，调用这个方法。返回的结果会显示在web的‘结果’一栏。
        '''
        requests.get
        attr_get = getattr(requests, config.get('method'))
        res = attr_get(
            (config.get('url')),
            headers={'User-Agent': config.get('User-Agent', 'Mozilla')}
        )
        return f'执行 {config} 成功：{res.text}'

    def get_conf_list(self):
        '''method 是 requests支持的请求方法，暂不支持 data/param 字段'''
        return {
            'url': '要访问的地址',
            'method': 'get, option, post',
            'User-Agent': '可选。访问时的客户端类型，默认为 Mozilla',
        }


CornReq.register()
