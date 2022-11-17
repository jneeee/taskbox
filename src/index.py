import json
from src.task.models import Tableclient


def lambda_handler(event, context):
    # TODO implement
    table = Tableclient('ddbtable')
    resp = table.get({'name': 'name1'})
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, resp: {resp}')
    }
