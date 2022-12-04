import logging

from src.task.models import Task
from src.utils import tools


LOG = logging.getLogger(__name__)

def get_single_task(task_id):
    if not task_id.startswith('Task_'):
        return {}
    res = Task.get_by_name(task_id)
    LOG.info(f'Quary task_id: {task_id}, res: {res}')
    return res

def get_task(req):
    if len(req.path_list) > 1:
        resp = get_single_task(req.path_list[1])
    else:
        resp = Task.get_all_tasks()

    return req.make_resp(tasks_list=resp, template_name='tasks.html')
