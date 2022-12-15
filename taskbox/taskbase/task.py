from os import getenv
import time

import boto3
from boto3.dynamodb.conditions import Attr, Key

from taskbox.utils.tools import LOG
from taskbox.taskbase.exception import TaskBaseException

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
class Tableclient():
    def __init__(self, tablename) -> None:
         _dynamo = boto3.resource('dynamodb')
         self.native_table = _dynamo.Table(tablename)

    def get(self, item):
        '''Get item by key

        item: dict{'id': key}
        return: dict({'id':xx, 'result':xx ...})
        '''

        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        resp = {}

        try:
            resp = self.native_table.get_item(Key=item).get("Item")
        except Exception as e:
            LOG.exception(e)
        return resp

    def delete(self, item):
        # item: dict{'id': key}
        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        self.native_table.delete_item(Key=item)

    def put(self, item):
        # item: dict{'id': id, 'value': value}
        # TODO threading
        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        self.native_table.put_item(Item=item)
        LOG.info(f'Put_item: {item}')

    def update(self, item):
        '''update item as dict.update

        item: {id:, val:,}
        return: None
        '''
        old = self.get({'id':item['id']})
        if isinstance(old, dict):
            old.update(item)
        else:
            old = item
        self.native_table.put_item(Item=old)


class Task(object):
    # format_seq for the desplay key seqence in web
    format_seq = ['名称', '状态', '结果', '上次执行', '消耗',
                  '累计消耗', '累计执行']
    task_dict = {}

    def __init__(self, *args, **kwargs):
        '''Create a Task instance

        :params kwargs: {
            id: str,
            status: normal|pedding|pause (correspond color green|yellow|red),
            result: str,
            conf:[{phone:xxx, passwd: xxx, }, ]} # can be multi config
            last_run_time: int, 1670907645.49549,
            exc_info = {
                cforce_cost: int, # the compute force cost
                run_count: int,
                total_cf_cost: int,
            }
        }
        '''
        self.type = self.__class__.__name__
        self.result = kwargs.get('result')
        self.conf = kwargs.get('conf', [])
        self.data_type = 'task_info'
        if 'last_run_time' in kwargs:
            self.run_time = kwargs.get('last_run_time')
        self.status = kwargs.get('status', 'pending')
        self.exc_info = kwargs.get('exc_info', {'cforce_cost': 0,
                                                'run_count': 0,
                                                'total_cf_cost': 0})

    @classmethod
    def register(cls):
        Task.task_dict[cls.__name__] = cls

    def step(self, config):
        '''Inplement with the task actually do

        :param config: dict, the single config dict for task
        :return: str, will be write to result
        :raise: raise a Exception that inherit from TaskBaseException
        '''
        raise NotImplementedError

    def run(self, context):
        '''Run task and save to db

        :param context: app context
        :return: None
        '''
        for config in self.conf:
            if self.status != 'normal':
                continue
            self.result = []
            self.exc_info['run_count'] += 1
            try:
                start = time.perf_counter()
                self.result.append(self.step(config))
                self.exc_info['cforce_cost'] = round(
                    (time.perf_counter()-start)*context.memory_limit_in_mb, 6
                )
                self.exc_info['total_cf_cost'] += self.exc_info['cforce_cost']
            except TaskBaseException as e:
                self.status = 'pedding' # or pause
                self.result.append(str(e))
            self.last_run_time = time.time()

            self._save()

    def get_conf_display(self):
        '''Implement me

        Remember to write the description. It will be desplaied at task detail
        web page.
        :return: a config dict with description and value
        '''
        raise NotImplementedError

    def _save(self):
        item = self.__dict__
        item['id'] = 'task_info'
        self.get_tb().put(item=item)
        LOG.info(f'Write to db: {item}')

    @classmethod
    def from_dict(cls, task_info):
        '''Create Task instance

        :param task_info: dict
        :return: Task_xxx instance
        '''
        return cls(**task_info)

    def get_history(self):
        return self.get_tb().native_table.query(
            KeyConditionExpression=Key('id').eq('task_history'),
            FilterExpression=Attr('type').eq(self.type),
        ).get('Items')

    @classmethod
    def get_by_name(cls, task_name):
        '''Get Task by name

        :param task_id: str
        :return: task dict
        '''
        res = cls.get_tb().native_table.query(
            KeyConditionExpression=Key('id').eq('task_info'),
            FilterExpression=Attr('type').eq(task_name)).get('Items')

        return res[0] if len(res) >= 1 else {}

    @classmethod
    def get_all_tasks(cls):
        '''Get all task list(latest)

        {"id":"Task_test", "data_type":"latest_log", "result":"OK!", "date":"2022-12-8"}
        TODO(jneeee) pagination
        :return: [{},]
        '''
        try:
            resp = cls.get_tb().native_table.query(
                FilterExpression=Key('id').eq('task_info'),
                Limit=20).get('Items')
        except:
            resp = [{},]
        return resp

    @property
    def info_format(self):
        if not hasattr(self, '_info_format'):
            self._info_format = self.ordereddict_format(self.__dict__)
        return self._info_format

    @classmethod
    def ordereddict_format(cls, task_d):
        '''Format a task dict

        :return: OrderedDict() with task info
        '''
        from collections import OrderedDict

        trans_d = {
            '名称': lambda d: d.get('type'),
            '状态': lambda d: d.get('status'),
            '结果': lambda d: d.get('result'),
            '上次执行': lambda d: time.strftime('%Y-%m-%d %H:%M:%S',
                time.localtime(d.get('last_run_time'))),
            '消耗': lambda d: d.get('exc_info', {}).get('cforce_cost'),
            '累计消耗': lambda d: d.get('exc_info', {}).get('total_cf_cost'),
            '累计执行': lambda d: d.get('exc_info', {}).get('run_count'),
        }
        res = OrderedDict()
        for name in cls.format_seq:
            res[name] = trans_d[name](task_d)
        return res

    @classmethod
    def get_tb(cls):
        '''Get Task table'''
        if not hasattr(cls, 'tb'):
            cls.tb = Tableclient(getenv('DDB_TABLE'))
        return cls.tb

    def registe_crontab(self, cron_str):
        pass


class Eventscheduler():

    def __init__(self, context) -> None:
        self.func_arn = context.invoked_function_arn
        self.client = boto3.client('scheduler')

    def create(self, name=None, ScheduleExpression=None):
        '''Create Eventbridge scheduler

        :param ScheduleExpression: string
            at(yyyy-mm-ddThh:mm:ss)
            rate(unit value)
            cron(minutes hours day_of_month month day_of_week year)
        :return: resp
        '''
        resp = self.client.create_schedule(
            Name=name,
            ScheduleExpression=ScheduleExpression,
            FlexibleTimeWindow={
                'Mode': 'OFF',
            },
            Target={'Arn': self.func_arn},
            RoleArn='',
            Input=''
        )
