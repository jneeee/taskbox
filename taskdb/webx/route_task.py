from taskdb.taskbase.object import Task
from taskdb.taskbase.manage import TaskManager
from taskdb.utils.tools import LOG


def get_task(req):
    # req.path_list = [task, Task_test]
    if len(req.path_list) > 1:
        task_id = req.path_list[1]
        task = TaskManager(task_id).task_inst
        return req.make_resp(task=task,
                             template_name='task_detail.html')
    else:
        return req.make_resp(tasks_list=Task.get_all_tasks(),
                             template_name='tasks.html')
