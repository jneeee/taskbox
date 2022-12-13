from taskdb.user_task.taskdemo import Task_demo


'''
TASK_LIST: Tell TaskDb where to find the task.
The key is task name, the value is where to find the task
will be called as:
    from value import key
'''
TASK_LIST = {
    'Task_demo': Task_demo,
}
