from taskbox.taskbase import exception
from taskbox.taskbase.task import Task, TaskList
from taskbox.taskbase.manage import TaskManager
from taskbox.utils.tools import auth_protect
from taskbox.utils.tools import LOG


@auth_protect
def get_task(req):
    # Display all task
    if len(req.path_list) == 1:
        if req.method == 'GET':
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

    elif len(req.path_list) == 3 and req.path_list[2] == 'log':
        if not req.is_authed:
            raise exception.NeedAuth('需要登录')
        task_id = req.path_list[1]
        task_mng = TaskManager(task_id)

        task_log_inst = task_mng.task_inst.get_log_inst()
        return req.make_resp(log_content=task_log_inst.get_latest_log_event(),
                             template_name='tasklog.html')

