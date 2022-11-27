import json
import logging

from src.utils import tools
from src.webx import (
    index,
    route_task,
    route_db,
)


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def lambda_handler(event, context):
    if not event.get('crontask'):
        path = tools.get_http_path(event)
        # path = ['task', <id>]
        paths = {
            'task': route_task.get_task,
            'db': route_db
        }
        if not path:
            return index.wsgi_root(event)
        return paths[path[0]](event)
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, event: {event}\ncontext: {context}')
    }
