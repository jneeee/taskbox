import os
import logging

import boto3
from moto import mock_dynamodb

from taskbox.utils.tools import LOG

LOG.setLevel(logging.DEBUG)

@mock_dynamodb
def create_table():
    os.environ['DDB_TABLE'] = 'table_name'
    table_param = dict(
        TableName='table_name',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'name',
                'AttributeType': 'S',
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    ddb = boto3.resource("dynamodb")
    table = ddb.create_table(**table_param)
    item = {'id': 'app_context', 'name': 'app', 'cur_authed_srip': []}
    table.put_item(Item=item)
    return table
