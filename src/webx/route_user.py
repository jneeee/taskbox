import json
import logging
import os

LOG = logging.getLogger()


def auth(req):
    '''perform /auth/login and /auth/logout'''
    path = req.path_list
    try:
        return eval(path[1])(req)
    except Exception as e:
        LOG.exception(e)
        req.msg = str(e)
        return req.make_resp(template_name='login.html')


def login(req):
    if req.method == 'GET':
        return req.make_resp(template_name='login.html')
    elif req.method == 'POST':
        req_passwd = json.loads(req.body.split('=')[1])

        if os.getenv('auth_passwd') == req_passwd:
            req.do_auth()
            msg = 'Login success!'
        else:
            msg = 'Login fail!'
        return req.make_resp(msg=msg, template_name='login.html')


def logout(req):
    req.do_auth_logout()
    return req.make_resp(msg='Logout success!', template_name='login.html')
