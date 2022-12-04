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
        item = req.body.split('=')[1]
        resp = models.get_app_db().put(item)
        return req.make_resp(put_res=resp, template_name='dynamodb.html')


def db_quary(event):
    pass
