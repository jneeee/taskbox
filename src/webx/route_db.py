import json
import logging

from src.task import models

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def route(req):
    path = req.path_list
    if len(path) == 1:
        return req.make_resp(template_name='dynamodb.html')
    elif path[1] == 'quary':
        # req.body = 'id=Task_xxx'
        key = req.body.split('=')[1]
        quary_res = models.get_app_db().get({'id': key})
        if not quary_res:
            req.msg = {'type': 'warning', 'info': f'No such key: {key}!'}
            return req.make_resp(template_name='dynamodb.html')
        return req.make_resp(quary_res=[quary_res,], template_name='dynamodb.html')
    elif path[1] == 'putitem':
        # req.body = 'item={'id':xx}'
        try:
            item = json.loads(req.body.split('=')[1])
            models.get_app_db().put(item)
            msg = f'Put item: {item}'
            req.msg = {'type': 'success', 'info': msg}
        except Exception as e:
            LOG.exception(e)
            req.msg = {'type': 'danger', 'info': e}
        return req.make_resp(template_name='dynamodb.html')
    elif path[1] == 'delete':
        try:
            LOG.info(f'Delete req.body: {req.body}')
            idstr = req.body.split('=')[1]
            models.get_app_db().delete({'id': idstr})
            req.msg = {'type': 'success', 'info': 'Delete success'}
        except Exception as e:
            LOG.exception(e)
            req.msg = {'type': 'danger', 'info': e}
        return req.make_resp(template_name='dynamodb.html')


def db_quary(event):
    pass
