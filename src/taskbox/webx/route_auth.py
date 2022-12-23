import os

from taskbox.utils.tools import LOG


def auth(req):
    '''perform /auth/login and /auth/logout'''
    path = req.path_list
    try:
        return eval(path[1])(req)
    except Exception as e:
        LOG.exception(e)
        req.msg = ('danger', e)
        return req.make_resp(template_name='login.html')


def login(req):
    if req.method == 'GET':
        return req.make_resp(template_name='login.html')
    elif req.method == 'POST':
        if os.getenv('auth_passwd') == req.body.get('passwd'):
            req.do_auth_login()
            req.msg = ('success', '登录成功!')
            req.is_authed = True
        else:
            req.msg = ('danger', '登录失败!')
        return req.make_resp(template_name='login.html')


def logout(req):
    req.do_auth_logout()
    req.msg = ('success', '登出成功!')
    req.is_authed = False
    return req.make_resp(template_name='login.html')
