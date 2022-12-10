from taskdb.utils.tools import LOG, run_cmd
from taskdb.webx.object import Request


def cmdhandler(req: Request):
    if req.method == 'GET':
        return req.make_resp(template_name='cmd.html')
    if not req.is_authed:
        req.msg = ('warning', '该操作需要登录!')
        return req.make_resp(template_name='cmd.html')

    key, val = req.body.split('=')
    if key == 'python':
        res = eval(val)
    elif key == 'shell':
        res = run_cmd(val)
    LOG.info(f'Run cmd: {val}, {res}')
    return req.make_resp(exc_res=res, template_name='cmd.html')
