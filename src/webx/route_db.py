import json
import logging

from src.task import models

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def route(req):
    path = req.path_list
    if len(path) == 1:
        return req.make_resp(template_name='dynamodb.html')
    elif req.method == 'POST':
        # req.body = 'id=Task_xxx'
        key, val = req.body.split('=')
        if key == 'quary_id':
            quary_res = models.get_app_db().get({'id': val})
            if not quary_res:
                req.msg = ('warning', f'No such key: {val}!')
                return req.make_resp(template_name='dynamodb.html')
            return req.make_resp(quary_res=[quary_res,], template_name='dynamodb.html')
        elif key == 'put_item':
            # req.body = 'item={'id':xx}'
            try:
                item = json.loads(val)
                models.get_app_db().put(item)
                req.msg = ('success', f'Put item: {item}')
            except Exception as e:
                LOG.exception(e)
                req.msg = ('danger', e)
            return req.make_resp(template_name='dynamodb.html')
    elif req.method == 'delete':
        try:
            LOG.info(f'Delete req.body: {req.body}')
            idstr = req.body.split('=')[1]
            models.get_app_db().delete({'id': idstr})
            req.msg = ('success', 'Delete success')
        except Exception as e:
            LOG.exception(e)
            req.msg = ('danger', e)
        return req.make_resp(template_name='dynamodb.html')


def db_quary(event):
    pass
