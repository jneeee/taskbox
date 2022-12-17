import unittest
from unittest import mock
import copy

from moto import mock_dynamodb

from taskbox.index import lambda_handler
from taskbox.utils.tools import LOG
from taskbox.tests import fixture
from taskbox.webx.object import Request


Fake_event = {
    "requestContext": {
        "http": {
            "method": "GET",
            "path": "/",
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
        cls.table = fixture.create_table()

    @classmethod
    def tearDownClass(cls):
        # cls.table.delete()
        pass

    def setUp(self):
        pass

    def test_get_tasks(self):
        resp = lambda_handler(Fake_event, Fake_context)
        self.assertIn('测试任务', resp.get('body'))

    def test_quary_single_task(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http']['path'] = '/task/Task_demo'
        resp = lambda_handler(tmp_event, Fake_context)
        self.assertIn('Task_demo', resp.get('body'))

    def test_run_cmd(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['headers'] = {'cmd': 'ls'}
        tmp_event['requestContext']['http']['path'] = '/cmd'

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
        self.assertIn('会话会在一天后过期', resp.get('body'))

    def test_auth_login_post(self):
        tmp_event = copy.deepcopy(Fake_event)
        tmp_event['requestContext']['http'].update(
            {'path': '/auth/login', 'method': 'POST'}
        )
        resp = lambda_handler(tmp_event, Fake_context)
        self.assertIn('登录失败', resp.get('body'))
