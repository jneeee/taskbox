import traceback

from taskdb.webx import object
from taskdb.utils.tools import LOG


def lambda_handler(event, context):
    req = object.Request(event)
    LOG.info(f'New {req}')

    try:
        return req.route()
    except Exception as e:
        LOG.exception(e)
        req.msg = ('danger', traceback.format_exc())
        return req.make_resp(template_name='release_note.html')
