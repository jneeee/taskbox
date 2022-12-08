import unittest
from unittest import mock
import copy
import logging

import boto3
from moto import mock_dynamodb

from src.task.models import Task
from src.index import lambda_handler

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

    def do_db_init(self):
        self.table.put_item(Item={'id': 'Task_foo', 'taskinfo': 'foo'})
        item = {'id': 'app_context', 'cur_authed_srip': []}
        self.table.put_item(Item=item)


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
        self.test_repo.do_db_init()

    def tearDown(self):
        self.table.delete()

    def test_get_tasks(self):
        lambda_handler(Fake_event, Fake_context)

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
        self.assertIn('Quary db', resp.get('body'))

    def test_auth_login_get(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http'].update(
            {'path': '/auth/login', 'method': 'GET'}
        )
        resp = lambda_handler(tmp_event, Fake_context)
        self.assertIn('Session will expire after one day.', resp.get('body'))

    def test_auth_login_post(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http'].update(
            {'path': '/auth/login', 'method': 'POST'}
        )
        tmp_event['body'] = b'aWQ9VGFza190ZXN0'
        import os
        os.getenv = mock.MagicMock()
        os.getenv.return_value = 'asd'
        resp = lambda_handler(tmp_event, Fake_context)
        self.assertIn('Login failed', resp.get('body'))
