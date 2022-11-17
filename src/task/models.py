import logging

import boto3

LOG = logging.getLogger(__name__)


class Tableclient():
    def __init__(self, dbname) -> None:
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(dbname)

    def get(self, key):
        # key: dict
        resp = None
        try:
            resp = self.table.get_item(Key=key)
        except Exception as e:
            LOG.error(e)
        return resp
