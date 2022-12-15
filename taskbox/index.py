import traceback

from taskbox.webx import object
from taskbox.utils.tools import LOG


def lambda_handler(event, context):
    try:
        req = object.Request(event, context)
        LOG.info(f'New {req}')
        return req.route()
    except Exception as e:
        LOG.exception(e)
        req.msg = ('danger', traceback.format_exc())
        return req.make_resp(template_name='release_note.html')
