import logging
from jinja2 import PackageLoader, Environment

from src.task.models import Task
from src.utils import tools


LOG = logging.getLogger(__name__)

def get_single_task(task_id):
    if not task_id.startswith('Task_'):
        return {}
    res = Task.get_by_name(task_id)
    LOG.info(f'Quary task_id: {task_id}, res: {res}')
    return res

def get_task(event):
    path = tools.get_http_path(event)
    if len(path) > 1:
        resp = get_single_task(path[1])
    else:
        resp = Task.get_all_tasks().get('Items')

    # if from browser, don't return json
    if 'curl' not in event.get('headers', {}).get('User-agent', ''):
        env = Environment(loader=PackageLoader('src.webx', 'templates'))
        template = env.get_template('tasks.html')
        resp = template.render(res=resp)

    return {
        'statusCode': 200,
        'body': resp,
    }
