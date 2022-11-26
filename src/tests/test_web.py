import unittest
from unittest import mock

import boto3

from src.index import lambda_handler

Fake_event = {
    "requestContext": {
        "http": {
            "method": "GET",
            "path": "/",
            "protocol": "HTTP/1.1",
            "sourceIp": "112.64.93.19",
            "userAgent": "Mozilla/5.0"
        },
    }
}

Fake_context = {}

class Test_web_tasks(unittest.TestCase):

    def test_get_tasks(self):
        Fake_task = {
            'id': 'task_abc',
            'value': 'value123',
        }
        boto3.resource('dynamodb').Table = mock.MagicMock()
        boto3.resource('dynamodb').Table.scan.return_value()
        print(lambda_handler(Fake_event, Fake_context))
