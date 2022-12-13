from taskdb.taskbase.models import Task, TaskManager
from taskdb.utils.tools import LOG

def get_single_task(task_id):
    if not task_id.startswith('Task_'):
        return {}
    res = TaskManager(task_id).display()
    LOG.info(f'Quary task_id: {task_id}, res: {res}')
    return res


def get_task(req):
    # req.path_list = [task, Task_test]
    if len(req.path_list) > 1:
        return req.make_resp(task=get_single_task(req.path_list[1]),
                             template_name='task_detail.html')
    else:
        return req.make_resp(tasks_list=Task.get_all_tasks(),
                             template_name='tasks.html')
