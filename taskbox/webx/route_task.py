from botocore.exceptions import ClientError

from taskbox.taskbase import exception
from taskbox.taskbase.task import Task, TaskList
from taskbox.taskbase.manage import TaskManager, Eventscheduler
from taskbox.utils.tools import LOG


class RouteTask():

    def __init__(self, req) -> None:
        pass


def get_task(req):
    if len(req.path_list) == 1:
        tasks_list = Task.get_all_tasks()
        taskl_obj = TaskList.from_list(tasks_list)

        # write new Task to db
        if len(tasks_list) != len(Task.task_dict):
            tasks_from_db = set(map(lambda i: i['name'], tasks_list))
            for name, obj in Task.task_dict.items():
                if name not in tasks_from_db:
                    task_obj = obj()
                    task_obj._save()
                    taskl_obj.append(task_obj)
                    LOG.info(f'init task {name}')
        return req.make_resp(taskl_obj=taskl_obj,
                             template_name='tasks.html')

    # req.path_list = [task, Task_test]
    elif len(req.path_list) > 1:
        task_id = req.path_list[1]
        task = TaskManager(task_id).task_inst

        # Deal with conf create
        if req.method == 'POST':
            if not req.is_authed:
                req.msg = ('danger', '该操作需要登录!')
            else:
                try:
                    if 'scheduler' in req.body:
                        _create_scheduler(task, req)
                    else:
                        _update_config(task, req)
                except exception.TaskBaseException as e:
                    req.msg = ('warning', e.args)
                else:
                    task._save()
        return req.make_resp(task=task,
                             template_name='task_detail.html')


def _create_scheduler(task, req):
    # create a scheduler, the name is taskname,
    expression = req.body.get('scheduler')

    try:
        if 'expression' in task.scheduler:
            Eventscheduler().update_schedule(name=task.name,
                                             ScheduleExpression=expression)
            req.msg = ('success', f'Update scheduler success: {expression}')
        else:
            Eventscheduler().create(name=task.name,
                                        ScheduleExpression=expression)
            req.msg = ('success', f'Create scheduler success: {expression}')
    except ClientError as e:
        req.msg = (f'warning', f'Create scheduler failed: {e}')
    else:
        task.scheduler = {'expression': expression}


def _update_config(task, req):
    acc = req.body.pop('account')
    if not acc:
        raise exception.TaskConfigInvalid('配置名称是必须的！')
    if 'delete' in req.body:
        task.conf.pop(acc)
    else:
        task.set_conf(acc, req.body)
    req.msg = ('success', f'Set conf Success: {req.body}')
