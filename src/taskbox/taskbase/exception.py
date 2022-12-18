class TaskBoxBaseException(Exception):
    pass

class TaskBaseException(Exception):
    pass

class TaskConfigInvalid(TaskBaseException):
    pass

class TaskExcuteError(TaskBaseException):
    pass
