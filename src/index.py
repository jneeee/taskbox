import json
import logging

import awsgi


LOG = logging.getLogger(__name__)

def lambda_handler(event, context):
    if not event.get('crontask'):
        from src.flaskapp import app
        return awsgi.response(app, event, context)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, event: {event}\ncontext: {context}')
    }
