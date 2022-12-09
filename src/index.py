import logging

from src.webx import object


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

def lambda_handler(event, context):
    req = object.Request(event)
    LOG.info(f'New {req}')

    try:
        return req.route()
    except Exception as e:
        LOG.exception(e)
        req.msg = ('danger', e)
        return req.make_resp(template_name='release_note.html')
