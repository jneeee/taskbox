import json

from taskbox.taskbase import task
from taskbox.utils.tools import auth_protect
from taskbox.utils.tools import LOG


@auth_protect
def route(req):
    if req.method == 'GET':
        return req.make_resp(template_name='dynamodb.html')
    elif req.method == 'POST':
        # op_type = 1 means query
        if req.body.get('op_type') == '1':
            query_item = {'id': req.body.get('id'), 'name': req.body.get('name')}
            quary_res = task.Task.get_tb().get(query_item)
            if not quary_res:
                req.msg = ('warning', f'No such key!: {query_item}')
                return req.make_resp(template_name='dynamodb.html')
            return req.make_resp(quary_res=[quary_res,], template_name='dynamodb.html')
        # op_type = 2 means delete
        elif req.body.get('op_type') == '2':
            query_item = {'id': req.body.get('id'), 'name': req.body.get('name')}
            try:
                task.Task.get_tb().delete(query_item)
                req.msg = ('success', f'Delete id: {query_item} success')
            except Exception as e:
                LOG.exception(e)
                req.msg = ('danger', e)
            return req.make_resp(template_name='dynamodb.html')
        elif req.body.get('op_type') == '3':
            # req.body = 'item={'id':xx, 'name':xx}'
            try:
                item = json.loads(req.body.get('put_item'))
                task.Task.get_tb().put(item)
                req.msg = ('success', f'Put item: {item}')
            except Exception as e:
                LOG.exception(e)
                req.msg = ('danger', e)
            return req.make_resp(template_name='dynamodb.html')
