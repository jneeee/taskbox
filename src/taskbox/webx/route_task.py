from taskbox.taskbase import exception
from taskbox.taskbase.task import Task, TaskList
from taskbox.taskbase.manage import TaskManager
from taskbox.utils.tools import auth_protect_if_not_get
from taskbox.utils.tools import LOG


def _get_task_detail(req):
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


@auth_protect_if_not_get
def get_task(req):
    # Display all task
    if len(req.path_list) == 1:
        if req.method == 'GET':
            return _get_task_detail(req)

    # req.path_list = [task, Task_name]
    # Single task
    elif len(req.path_list) == 2:
        task_id = req.path_list[1]
        task_mng = TaskManager(task_id)

        # Deal with conf create
        if req.method == 'POST':
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

    elif len(req.path_list) >= 3 and req.path_list[2] == 'log':
        if not req.is_authed:
            raise exception.NeedAuth('需要登录')

        LOG.info(f'Get log detail, req_path: {req.path_list}')
        task_id = req.path_list[1]
        task_log_inst = TaskManager(task_id).task_inst.log_inst

        log_detail = task_log_inst.get_log_event_by_reqid(req.path_list[3])
        return req.make_resp(
            content=f'<h4>任务日志</h4><p>{log_detail}</p>',
            template_name='escape.html')
