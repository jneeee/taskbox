import os

import boto3

from moto import mock_dynamodb

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
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    ddb = boto3.resource("dynamodb")
    table = ddb.create_table(**table_param)
    table.put_item(Item={'id': 'Task_foo', 'taskinfo': 'foo'})
    item = {'id': 'app_context', 'cur_authed_srip': []}
    table.put_item(Item=item)
    return table
