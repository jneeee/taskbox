import logging

import boto3

LOG = logging.getLogger(__name__)


class Tableclient():
    def __init__(self, tablename) -> None:
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(tablename)

    def get(self, item):
        # item: dict{'id': key}
        if not isinstance(item, dict):
            return False
        resp = None
        try:
            resp = self.table.get_item(Key=item).get("Item")
        except Exception as e:
            LOG.error(e)
        return resp

    def delete(self, item):
        # item: dict{'id': key}
        if not isinstance(item, dict):
            return False
        self.table.delete_item(Item=item)

    def put_item(self, item):
        # item: dict{'id': id, 'value': value}
        if not isinstance(item, dict):
            return False
        self.table.put_item(Item=item)
        LOG.info(f'Put_item: {item}')


def Task(object):
    def __init__(self):
        self.name = self.__name__
        self.result = None

    def run(self):
        raise NotImplementedError
