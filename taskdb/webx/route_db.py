import json

from taskdb.taskbase import object
from taskdb.utils.tools import LOG


def route(req):
    if req.method == 'GET':
        return req.make_resp(template_name='dynamodb.html')
    elif req.method == 'POST':
        if not req.is_authed:
            req.msg = ('warning', '该操作需要登录!')
            return req.make_resp(template_name='dynamodb.html')

        # req.body = 'id=Task_xxx'
        key, val = req.body.split('=')
        if key == 'quary_id':
            quary_res = object.get_app_db().get({'id': val})
            if not quary_res:
                req.msg = ('warning', f'No such key!: {val}')
                return req.make_resp(template_name='dynamodb.html')
            return req.make_resp(quary_res=[quary_res,], template_name='dynamodb.html')

        elif key == 'put_item':
            # req.body = 'item={'id':xx}'
            try:
                item = json.loads(val)
                object.get_app_db().put(item)
                req.msg = ('success', f'Put item: {item}')
            except Exception as e:
                LOG.exception(e)
                req.msg = ('danger', e)
            return req.make_resp(template_name='dynamodb.html')

        elif key == 'delete_id':
            try:
                object.get_app_db().delete({'id': val})
                req.msg = ('success', f'Delete id: {val} success')
            except Exception as e:
                LOG.exception(e)
                req.msg = ('danger', e)
            return req.make_resp(template_name='dynamodb.html')


def db_quary(event):
    pass
