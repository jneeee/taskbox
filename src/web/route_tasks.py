from flask import render_template

from boto3.dynamodb.conditions import Attr
from boto3 import resource

from src.task.models import Task


def get_tasks():
    table = resource('dynamodb').Table(Task.tablename)
    resp = table.scan(
        FilterExpression=Attr('id').begins_with('task_')
    )
    data = {
        'content': resp['Items'],
    }
    return render_template('index.html', **data)
