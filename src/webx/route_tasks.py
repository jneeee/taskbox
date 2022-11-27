from json import dumps

from boto3.dynamodb.conditions import Attr
from boto3 import resource

from src.task.models import Task

def get_tasks(*args):
    table = resource('dynamodb').Table(Task.tablename)
    resp = table.scan(
        FilterExpression=Attr('id').begins_with('task_')
    )
    data = {
        'content': resp['Items'],
    }
    return {
        'statusCode': 200,
        'body': dumps(data),
    }
