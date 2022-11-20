import json
import logging

from src.task.models import Tableclient

LOG = logging.getLogger(__name__)

def lambda_handler(event, context):
    # TODO implement
    if not event.get('crontask'):
        from src.flaskapp import app
        return app(event, context)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, event: {event}\ncontext: {context}')
    }
