from os import getenv
import time

import boto3
from boto3.dynamodb.conditions import Attr

from taskdb.utils.tools import LOG

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

    def __init__(self):
        self.name = self.__class__.__name__
        self.CONF = Task.tb.get({'id': f'conf_{self.name}'})
        self.result = None

    def step(self):
        # overwrite me
        # update self.result in this func
        raise NotImplementedError

    def run(self):
        # run task and save to db
        self.step()
        self.last_run_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self._save()

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
        '''Get task by name

        task_id: str
        return: dict()
        '''
        res = cls.tb.get({'id': task_id})
        return res or {}

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
