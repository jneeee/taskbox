import json
import logging

from src import web

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def lambda_handler(event, context):
    if not event.get('crontask'):
        req = event['requestContext']['http']['path'].lstrip('/')
        operations = {
            '/': web.wsgi_root,
            '/tasks': web.route_tasks.get_tasks,
        }
        return operations[operation](event.get('payload'))
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, event: {event}\ncontext: {context}')
    }
