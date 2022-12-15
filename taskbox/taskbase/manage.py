from taskbox.taskbase.task import Task
from taskbox.user_task import *


class TaskManager():
    '''TaskManager'''

    def __init__(self, task_name) -> None:
        self.task_name = task_name
        self._task_info = None

    @property
    def task_info(self):
        if not self._task_info:
            self._task_info = Task.get_by_name(self.task_name)
        return self._task_info

    @property
    def task_inst(self):
        task_cls = Task.task_dict.get(self.task_name)
        if not task_cls:
            raise ModuleNotFoundError
        return task_cls(**self.task_info)

    def get_dict_info(self):
        '''display task info

        if task have multi config, we should return multi task history
        :return: OrderedDict() with task info
        '''
        return self.task_inst.info_format

    def pause(self):
        # TODO
        Task.get_by_name(self.task_name)
        pass

    def create_scheduler(self):
        pass

    def run(self):
        self.task_inst.run()
