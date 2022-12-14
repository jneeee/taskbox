import taskdb.conf as CONF
from taskdb.taskbase.models import Task
from taskdb.user_task import *

class TaskManager():
    '''TaskManager'''

    def __init__(self, task_id) -> None:
        self.task_id = task_id

    @property
    def task_info(self):
        if not self._task_info:
            self._task_info = Task.get_by_name(self.task_id)
        return self._task_info

    @property
    def task_inst(self):
        task_cls = Task.task_dict.get(self.task_id)
        if not task_cls:
            raise ModuleNotFoundError
        return task_cls(**self.task_info)

    def display(self):
        '''display task info

        if task have multi config, we should return multi task history
        :return: OrderedDict() with task info
        '''
        return self.task.info_format

    def pause(self):
        # TODO
        Task.get_by_name(self.task_id)
        pass

    def create_scheduler(self):
        pass

    def run(self):
        self.task_inst.run()
