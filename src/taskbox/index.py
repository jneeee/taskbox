import traceback

from taskbox.webx import object
from taskbox.utils.tools import LOG
from taskbox.taskbase.manage import TaskManager

def lambda_handler(event, context):
    if event.get('Excutetask'):
        LOG.info(f'Event from scheduler: {event}')
        return TaskManager(event.get('Excutetask')).run()
    try:
        req = object.Request(event, context)
        LOG.info(f'New {req}')
        return req.route()
    except Exception as e:
        LOG.warning(f'event: {event}, context: {context}')
        LOG.exception(e)
