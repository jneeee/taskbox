from taskbox.utils.tools import LOG, run_cmd


def cmdhandler(req):
    if req.method == 'GET':
        return req.make_resp(template_name='cmd.html')
    if not req.is_authed:
        req.msg = ('warning', '该操作需要登录!')
        return req.make_resp(template_name='cmd.html')

    if 'python' in req.body:
        # Add module if need.
        import requests, time
        res = eval(req.body.get('python'))
    elif 'shell' in req.body:
        val  = req.body.get('shell')
        cmdres = run_cmd(val)
        if cmdres[0]:
            res = f'🟢$ {val}</p><p>{cmdres[0]}'
        else:
            res = f'🔴$ {val}</p><p>{cmdres[1]}'
        LOG.info(f'Run cmd: {val}, {res}')
    return req.make_resp(exc_res=res, template_name='cmd.html')
