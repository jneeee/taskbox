from taskbox.webx import object
from taskbox.utils.tools import LOG
from taskbox.taskbase.manage import TaskManager
from taskbox.taskbase.exception import TaskBaseException


def lambda_handler(event, context):
    # Deal with scheduler task
    if event.get('Excutetask'):
        LOG.info(f'Event from scheduler: {event}')
        TaskManager(event.get('Excutetask')).run(context)
        return

    # Web req
    try:
        req = object.Request(event, context)
        LOG.info(f'New {req}')
        return req.route()
    except TaskBaseException as e:
        LOG.exception(e)
        req.msg = ('danger', e)
        req.make_resp(http_code=403)
    except Exception as e:
        LOG.exception(e)
        req.make_resp(http_code=404)
