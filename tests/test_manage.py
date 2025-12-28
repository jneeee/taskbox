import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from taskbox.tests.fixture import create_table
from taskbox.taskbase.manage import TaskManager

class Test_manage(unittest.TestCase):

    def setUp(self) -> None:
        self.table = create_table()
        d = {
            'DDB_TABLE': 'table_name',
            'AWS_ACCESS_KEY_ID': "keyid",
            'AWS_SECRET_ACCESS_KEY': "AWS_SECRET_ACCESS_KEY",
            'AWS_SESSION_TOKEN': "AWS_SESSION_TOKEN",
        }
        os.environ.update(d)
        return super().setUp()

    def test_not_exsit_task(self):
        self.assertRaises(FileNotFoundError, TaskManager, 'asdasd')

    def test_taskdemo(self):
        TaskManager('Task_demo')
