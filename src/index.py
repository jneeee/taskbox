import logging

from src.utils import tools
from src.webx import (
    object,
)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def lambda_handler(event, context):
    if not event.get('crontask'):
        req = object.Request(event)
        LOG.info(f'Get http request path: {req.path_list}')

        try:
            return req.route()
        except Exception as e:
            LOG.exception(e)
            return str(e)
