import traceback

from taskbox.webx import object
from taskbox.utils.tools import LOG
from taskbox.taskbase.manage import TaskManager

def lambda_handler(event, context):
    if event.get('Excutetask'):
        TaskManager.run(event.get('Excutetask'), context)
    try:
        req = object.Request(event, context)
        LOG.info(f'New {req}')
        return req.route()
    except Exception as e:
        LOG.warning(f'event: {event}, context: {context}')
        LOG.exception(e)
        req.msg = ('danger', traceback.format_exc())
        return req.make_resp(template_name='404.html')
