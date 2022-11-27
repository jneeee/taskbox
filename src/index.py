import json
import logging

from src import webx
from src.webx import index
from src.webx import route_tasks


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def lambda_handler(event, context):
    if not event.get('crontask'):
        path = event['requestContext']['http']['path']
        paths = {
            '/': index.wsgi_root,
            '/tasks': route_tasks.get_tasks,
        }
        return paths[path](event)
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, event: {event}\ncontext: {context}')
    }
