import os
import unittest
from unittest import mock
import copy

import boto3
from moto import mock_dynamodb

from taskdb.index import lambda_handler
from taskdb.utils.tools import LOG

os.environ['DDB_TABLE'] = 'table_name'


def create_user_table() -> dict:
    return dict(
        TableName='table_name',
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

    def __init__(self, ddb_resource):
        if not ddb_resource:
            ddb_resource = boto3.resource('dynamodb')
        self.table = ddb_resource.Table('table_name')

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
    },
    'body': b'aWQ9VGFza190ZXN0',
}

Fake_context = {}


@mock_dynamodb
class Test_web_tasks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env_patcher = mock.patch.dict(os.environ, {"DDB_TABLE": "table_name"})
        cls.env_patcher.start()
        super().setUpClass()

    def setUp(self):
        ddb = boto3.resource("dynamodb")
        self.table = ddb.create_table(**create_user_table())
        self.test_repo = TaskRepository(ddb)
        self.test_repo.do_db_init()

    def tearDown(self):
        self.table.delete()

    def test_get_tasks(self):
        resp = lambda_handler(Fake_event, Fake_context)
        print(resp.get('body'))
        self.assertIn('Task', resp.get('body'))

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
            {'path': '/db', 'method': 'POST'}
        )
        resp = lambda_handler(tmp_event, Fake_context)
        self.assertIn('Quary db', resp.get('body', None))

    def test_db_putitem(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http'].update(
            {'path': '/db', 'method': 'POST'}
        )
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
        import os
        os.getenv = mock.MagicMock()
        os.getenv.return_value = 'asd'
        resp = lambda_handler(tmp_event, Fake_context)
        self.assertIn('Login failed', resp.get('body'))
