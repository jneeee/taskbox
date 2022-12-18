from taskbox.taskbase import exception
from taskbox.taskbase.task import Task, TaskList
from taskbox.taskbase.manage import TaskManager
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
        task_mng = TaskManager(task_id)

        # Deal with conf create
        if req.method == 'POST':
            if not req.is_authed:
                req.msg = ('danger', '该操作需要登录!')
            else:
                try:
                    if 'scheduler' in req.body:
                        task_mng.update_scheduler(req)
                    else:
                        task_mng.update_config(req)
                except exception.TaskBaseException as e:
                    req.msg = ('warning', e.args)
                else:
                    task_mng.task_inst._save()
        return req.make_resp(task=task_mng.task_inst,
                             template_name='task_detail.html')
