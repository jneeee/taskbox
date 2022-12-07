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
        quary_res = models.get_app_db().get({'id': req.body.split('=')[1]})
        return req.make_resp(quary_res=[quary_res,], template_name='dynamodb.html')
    elif path[1] == 'putitem':
        # req.body = 'item={'id':xx}'
        try:
            item = json.loads(req.body.split('=')[1])
            resp = models.get_app_db().put(item)
            LOG.info(f'{req}, put item: {item}')
        except json.decoder.JSONDecodeError:
            resp = 'Json decode error!'
        return req.make_resp(warn_msg=resp, template_name='dynamodb.html')
    elif path[1] == 'delete':
        try:
            LOG.info(f'Delete req.body: {req.body}')
            idstr = req.body.split('=')[1]
            exe_res = models.get_app_db().delete({'id': idstr})
        except Exception as e:
            LOG.exception(e)
            exe_res = str(e)
        return req.make_resp(warn_msg=exe_res, template_name='dynamodb.html')


def db_quary(event):
    pass
