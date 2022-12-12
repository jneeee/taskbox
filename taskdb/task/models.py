from os import getenv
import time

import boto3
from boto3.dynamodb.conditions import Attr

from taskdb.utils.tools import LOG
from taskdb.task.exception import TaskBaseException

TASK_LIST_KEY = 'task_list'

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
class Tableclient():
    def __init__(self, tablename) -> None:
         _dynamo = boto3.resource('dynamodb')
         self.table = _dynamo.Table(tablename)

    def get(self, item):
        '''Get item by key

        item: dict{'id': key}
        return: dict({'id':xx, 'result':xx ...})
        '''

        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        resp = None

        try:
            resp = self.table.get_item(Key=item).get("Item")
        except Exception as e:
            LOG.exception(e)
        return resp

    def delete(self, item):
        # item: dict{'id': key}
        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        self.table.delete_item(Key=item)

    def put(self, item):
        # item: dict{'id': id, 'value': value}
        # TODO threading
        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        self.table.put_item(Item=item)
        LOG.info(f'Put_item: {item}')

    def update(self, item):
        '''update item as dict.update

        item: {id:, val:,}
        return: None
        '''
        old = self.get({'id':item['id']})
        old.update(item)
        self.table.put_item(Item=old)


def get_app_db():
    return Tableclient(getenv('DDB_TABLE'))


class Task():
    tb = Tableclient(getenv('DDB_TABLE'))
    # format_seq for the desplay key seqence in web
    format_seq = ['名称', '状态', '结果', '上次执行时间', '消耗', '累计消耗', '累计执行次数']

    def __init__(self, **kwargs):
        '''Create a Task instance

        the kwargs expected:{
            id: str, status: normal|pedding|pause (with correspond color
                green|yellow|red),
            result: str,
            conf:[{phone:xxx, passwd: xxx, }, ]} # can be multi config
            last run time: '2022-12-12 16:57:11',
            cforce_cost: int, # the compute force cost
            run_count: int,
            total_cf_cost: int,
        }
        '''
        self.name = self.__class__.__name__
        for key, val in kwargs.items():
            setattr(self, key, val)

    def step(self, config):
        '''Inplement with the task actually do

        need update self.result in this func
        :param config: dict, the config dict for task
        :return: True if task success
        :raise: raise a Exception that inherit from TaskBaseException
        '''
        raise NotImplementedError

    def run(self, config_list):
        # run task and save to db
        for config in config_list:
            self.total_count += 1
            try:
                self.step(config)
            except TaskBaseException:
                pass
            self.last_run_time = time.strftime('%Y-%m-%d', 
                                               time.localtime(time.time()))
            self._save()

    def get_conf(self):
        '''Implement me

        Remember to write the description. It will be desplaied at task detail web page.
        :return: a config dict with description and value
        '''
        raise NotImplementedError

    def _save(self):
        item = {'id': self.name}
        item['date'] = self.last_run_time
        item['result'] = self.result
        item['data_type'] = 'latest_log'

        self.tb.put(item)
        LOG.info(f'Update task: {item}')

    @classmethod
    def from_dict(cls):
        pass

    def get_history(self):
        item = {'id': self.name}
        resp = self.tb.get(item)
        return resp

    @classmethod
    def get_by_name(cls, task_id):
        '''Get Task by name

        :param task_id: str
        :return: Task instance
        '''
        task_info = cls.tb.get({'id': task_id})
        return cls.from_dict(task_info)

    @classmethod
    def get_all_tasks(cls):
        '''Get all task list(latest)

        return [{},]
        {"id":"Task_test", "data_type":"latest_log", "result":"OK!", "date":"2022-12-8"}
        '''
        try:
            resp = cls.tb.table.scan(
            FilterExpression=Attr('id').begins_with('Task_') & Attr('data_type').eq('latest_log')
        ).get('Items')
        except:
            resp = [{},]
        return resp

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
            Target={'Arn': self.func_arn}
            RoleArn='',
            Input=''
        )
