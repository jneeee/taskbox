from flask import Blueprint
from flask import render_template

from boto3.dynamodb.conditions import Attr
from boto3 import resource

from src.task.models import Task


bp_tasks = Blueprint('tasks', __name__)

@bp_tasks.route('/list')
def get_db():
    table = resource('dynamodb').Table(Task.tablename)
    resp = table.scan(
        FilterExpression=Attr('id').begins_with('task_')
    )
    data = {
        'content': resp['Items'],
    }
    return render_template('index.html', **data)
