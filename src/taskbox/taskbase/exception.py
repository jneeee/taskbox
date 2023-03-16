class TaskBaseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class TaskConfigInvalid(TaskBaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class TaskExcuteError(TaskBaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NeedAuth(TaskBaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
