import time
import logging

import boto3

LOG = logging.getLogger(__name__)

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
class Tableclient(boto3.resource('dynamodb').Table):
    def __init__(self, tablename) -> None:
        super().__init__(tablename)

    def get(self, item):
        # item: dict{'id': key}
        if not isinstance(item, dict):
            return False
        resp = None
        try:
            resp = self.get_item(Key=item).get("Item")
        except Exception as e:
            LOG.error(e)
        return resp

    def delete(self, item):
        # item: dict{'id': key}
        if not isinstance(item, dict):
            return False
        self.delete_item(Item=item)

    def put(self, item):
        # item: dict{'id': id, 'value': value}
        if not isinstance(item, dict):
            return False
        self.put_item(Item=item)
        LOG.info(f'Put_item: {item}')


def Task(object):
    tablename = 'appname-ddbTable-1TUAC9NKUUB7F'
    def __init__(self):
        self.name = 'task_%s' % self.__name__
        self.result = None
        self.table = Tableclient(self.tablename)

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

        self.table.put(item)
        LOG.info(f'Update task: {item}')

    def from_dict(cls):
        pass

    def get_history(self):
        item = {'id': self.name}
        resp = self.table.get(item)
        return resp
