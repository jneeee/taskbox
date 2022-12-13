from taskdb.task.models import Task


class Task_demo(Task):

    def __init__(self):
        super().__init__()

    def step(self):
        return 'Run success!'

    def get_conf_list(self):
        '''Config for task Demo_task
        
        This will display in task detail page.
        :configkey1: content configkey1 description
        :configkey2: content configkey2 description
        '''
        return ['configkey1', 'configkey2']
