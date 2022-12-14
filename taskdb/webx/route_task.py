from taskdb.taskbase.object import Task
from taskdb.taskbase.manage import TaskManager
from taskdb.utils.tools import LOG


def get_single_task(task_id):
    res = TaskManager(task_id).get_dict_info()
    LOG.info(f'Quary task_id: {task_id}, res: {res}')
    return res


def get_task(req):
    # req.path_list = [task, Task_test]
    if len(req.path_list) > 1:
        task_id = req.path_list[1]
        task = TaskManager(task_id)
        return req.make_resp(task=task,
                             template_name='task_detail.html')
    else:
        return req.make_resp(tasks_list=Task.get_all_tasks(),
                             template_name='tasks.html')
