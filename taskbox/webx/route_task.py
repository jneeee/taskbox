from taskbox.taskbase.task import Task, TaskList
from taskbox.taskbase.manage import TaskManager
from taskbox.utils.tools import LOG


def get_task(req):
    # req.path_list = [task, Task_test]
    if len(req.path_list) > 1:
        task_id = req.path_list[1]
        task = TaskManager(task_id).task_inst
        return req.make_resp(task=task,
                             template_name='task_detail.html')

    else:
        tasks_list = Task.get_all_tasks()
        taskl_obj = TaskList.from_list(tasks_list)

        # import pdb;pdb.set_trace()
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
