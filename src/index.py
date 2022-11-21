import json
import logging

import awsgi


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def lambda_handler(event, context):
    if not event.get('crontask'):
        from flask import Flask
        from src.flaskapp.route_db import bp_tasks
        from src.flaskapp import root_path
        app = Flask(__name__, template_folder='src/flaskapp/templates')
        app.debug = True
        app.register_blueprint(bp_tasks)
        app.register_blueprint(root_path)
        return awsgi.response(app, event, context)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, event: {event}\ncontext: {context}')
    }
