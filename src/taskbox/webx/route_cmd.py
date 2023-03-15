from taskbox.utils.tools import LOG, run_cmd
from taskbox.utils.tools import auth_protect_if_not_get


@auth_protect_if_not_get
def cmdhandler(req):
    if req.method == 'GET':
        return req.make_resp(template_name='cmd.html')

    if 'python' in req.body:
        # Add module if need.
        res = None
        try:
            import requests, time
            res = eval(req.body.get('python'))
        except NameError:
            req.msg = ('warning', '错误的Python语法!')
        return req.make_resp(exc_res=res, template_name='cmd.html')
    elif 'shell' in req.body:
        val  = req.body.get('shell')
        cmdres = run_cmd(val)
        if cmdres[0]:
            res = f'🟢$ {val}</p><p>{cmdres[0]}'
        else:
            res = f'🔴$ {val}</p><p>{cmdres[1]}'
        LOG.info(f'Run cmd: {val}, {res}')
        return req.make_resp(exc_res=res, template_name='cmd.html')
