import unittest
import copy
import logging

import boto3
from moto import mock_dynamodb

from src.task.models import Task
from src.index import lambda_handler
from src.webx import route_task

LOG = logging.getLogger()

def create_user_table(table_name: str) -> dict:
    return dict(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )


class TaskRepository:
    table_name = Task.tablename

    def __init__(self, ddb_resource):
        if not ddb_resource:
            ddb_resource = boto3.resource('dynamodb')
        self.table = ddb_resource.Table(self.table_name)

    def create_task(self, taskinfo):
        return self.table.put_item(Item={'id': f'Task_{taskinfo}', 'taskinfo': taskinfo})


Fake_event = {
    "requestContext": {
        "http": {
            "method": "GET",
            "path": "/task",
            "protocol": "HTTP/1.1",
            "sourceIp": "112.64.93.19",
            "userAgent": "Mozilla/5.0"
        },
    }
}

Fake_context = {}

@mock_dynamodb
class Test_web_tasks(unittest.TestCase):

    def setUp(self):
        ddb = boto3.resource("dynamodb")
        self.table = ddb.create_table(**create_user_table(Task.tablename))
        self.test_repo = TaskRepository(ddb)
        self.test_repo.create_task('foo')

    def tearDown(self):
        self.table.delete()

    def test_get_tasks(self):
        print(lambda_handler(Fake_event, Fake_context))

    def test_quary_single_task(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http']['path'] = '/task/Task_foo'
        print(lambda_handler(tmp_event, Fake_context))

    def test_run_cmd(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['headers'] = {'cmd': 'ls'}
        tmp_event['requestContext']['http']['path'] = '/cmd'
        print(lambda_handler(tmp_event, Fake_context))

    def test_db_query(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http'].update(
            {'path': '/db/quary', 'method': 'POST'}
        )
        tmp_event['body'] = b'aWQ9VGFza190ZXN0'
        resp = lambda_handler(tmp_event, Fake_context)
        LOG.error(f'========\n resp: {resp}')
        self.assertIn('Quary db', resp.get('body'))

    def test_db_putitem(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http'].update(
            {'path': '/db/quary', 'method': 'POST'}
        )
        tmp_event['body'] = b'aWQ9VGFza190ZXN0'
        resp = lambda_handler(tmp_event, Fake_context)
        LOG.info(f'========\n resp: {resp}')
        self.assertIn('Quary db', resp.get('body'))
