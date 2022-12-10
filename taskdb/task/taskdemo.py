from taskdb.task.models import Task


class Demo_task(Task):

    def __init__(self):
        super().__init__()

    def step(self):
        self.result = 'Run success!'

