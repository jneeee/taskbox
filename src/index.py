import json
import logging

from src.task.models import Tableclient

LOG = logging.getLogger(__name__)

def lambda_handler(event, context):
    LOG.info(f'event: {event}')
    LOG.info(f'context: {context}')
    # TODO implement
    table = Tableclient('ddbtable')
    resp = table.put_item(key='123', value='345')
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, put_item resp: {resp}\nevent: {event}\ncontext: {context}')
    }
