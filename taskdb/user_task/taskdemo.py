from taskdb.taskbase.models import Task


__all__ = ['Task_demo']


class Task_demo(Task):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def step(self):
        conf1 = self.conf.get('configkey1')
        return f'conf1: {conf1}, Run success!'

    def get_conf_list(self):
        '''Config for task Demo_task

        This will display in task detail page.
        scheduler 配置推荐(文字说明): xxxx
        :configkey1: content configkey1 description
        :configkey2: content configkey2 description
        '''
        return ['configkey1', 'configkey2']

Task_demo.register()
