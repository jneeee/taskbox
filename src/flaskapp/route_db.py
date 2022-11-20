from flask import render_template

from boto3.dynamodb.conditions import Attr

from src.task.models import Task, Tableclient
from src.flaskapp import app


@app.route('/task')
def get_db():
    table = Tableclient(Task.tablename)
    resp = table.scan(
        FilterExpression=Attr('id').begins_with('task_')
    )
    data = {
        'content': resp['Items'],
    }
    return render_template('index.html', **data)
