from os import getenv

import boto3
from botocore.exceptions import ClientError

from taskbox.taskbase import task
from taskbox import user_task # noqa


class TaskManager():
    '''TaskManager'''

    def __init__(self, task_name) -> None:
        if task_name not in task.Task.task_dict:
            raise FileNotFoundError
        self.task_name = task_name
        self._task_info = None

    @property
    def task_info(self):
        if not self._task_info:
            self._task_info = task.Task.get_by_name(self.task_name)
        return self._task_info

    @property
    def task_inst(self):
        task_cls = task.Task.task_dict.get(self.task_name)
        if not task_cls:
            raise ModuleNotFoundError
        return task_cls(**self.task_info)

    def get_dict_info(self):
        '''display task info

        if task have multi config, we should return multi task history
        :return: OrderedDict() with task info
        '''
        return self.task_inst.info_format

    def pause(self):
        # TODO
        task.Task.get_by_name(self.task_name)
        pass

    def create_scheduler(self):
        pass

    def run(self):
        self.task_inst.run()


class Eventscheduler():

    def __init__(self) -> None:
        self.func_arn = getenv('FUNC_ARN')
        self.client = boto3.client('scheduler')

    def create(self, name=None, ScheduleExpression=None):
        '''Create Eventbridge scheduler

        :param ScheduleExpression: string
            at(yyyy-mm-ddThh:mm:ss)
            rate(unit value)
            cron(minutes hours day_of_month month day_of_week year)
        :return: resp
        '''
        try:
            resp = self.client.create_schedule(
                Name=name,
                ScheduleExpression=ScheduleExpression,
                ScheduleExpressionTimezone='Asia/Shanghai',
                FlexibleTimeWindow={
                    'Mode': 'OFF',
                },
                Target={
                    'Arn': self.func_arn,
                    'RoleArn': 'arn:aws:iam::044694559979:role/mytaskdb-TaskdashboardRole-L505MACM0I2U',
                    'Input': f'{"Excutetask": "{name}"}',
                },
                # Cloudfoundtion will create exc role with func logical name
                # RoleArn=getenv('ROLE_ARN'),
            )
        except ClientError as e:
            raise e
        return resp

    def update_schedule(self, name=None, ScheduleExpression=None):
        self.client.update_schedule(
            Name=name,
            ScheduleExpression=ScheduleExpression,
            ScheduleExpressionTimezone='Asia/Shanghai',
            FlexibleTimeWindow={
                'Mode': 'OFF',
            },
            Target={
                'Arn': self.func_arn,
                'RoleArn': 'arn:aws:iam::044694559979:role/mytaskdb-TaskdashboardRole-L505MACM0I2U',
                'Input': f'{"Excutetask": "{name}"}',
            },
            # Cloudfoundtion will create exc role with func logical name
            # RoleArn=getenv('ROLE_ARN'),
        )

    def list_schedules(self):
        pass

    def delete_scheduler(self):
        pass
