import time
import logging

import boto3
from boto3.dynamodb.conditions import Attr

LOG = logging.getLogger(__name__)
TASK_LIST_KEY = 'task_list'

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
class Tableclient():
    def __init__(self, tablename) -> None:
         _dynamo = boto3.resource('dynamodb')
         self.table = _dynamo.Table(tablename)

    def get(self, item):
        '''Get item by key

        item: dict{'id': key}
        return dict({'id':xx, 'result':xx ...})
        '''

        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        resp = None

        try:
            resp = self.table.get_item(Key=item).get("Item")
        except Exception as e:
            LOG.error(e)
        return resp

    def delete(self, item):
        # item: dict{'id': key}
        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        self.table.delete_item(Key=item)
        return f'Delete {item} success!'

    def put(self, item):
        # item: dict{'id': id, 'value': value}
        # TODO threading
        if not isinstance(item, dict):
            raise ValueError('Tableclient: item is not a dict')
        self.table.put_item(Item=item)
        LOG.info(f'Put_item: {item}')

    def quary_begins_with(self, pre):
        # return [{},]
        return self.table.scan(
            FilterExpression=Attr('id').begins_with(pre)
        ).get('Items')


def get_app_db():
    tablename = 'appname-ddbTable-1TUAC9NKUUB7F'
    return Tableclient(tablename)


class Task():
    tablename = 'appname-ddbTable-1TUAC9NKUUB7F'
    tb = Tableclient(tablename)

    def __init__(self):
        self.name = self.__class__.__name__
        self.result = None

    def step(self):
        # overwrite me
        # update self.result in this func
        raise NotImplementedError

    def run(self):
        self.step()
        self.last_run_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self._save()

    def _save(self):
        item = {'id': self.name}
        item['last_run_time'] = self.last_run_time
        item['result'] = self.result

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
        return cls.tb.get({'id': task_id})

    @classmethod
    def get_all_tasks(cls):
        # return [{},]
        return cls.tb.quary_begins_with('Task_')

    def registe_crontab(cron_str):
        pass
