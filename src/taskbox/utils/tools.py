import datetime
import subprocess
import logging


def _beijing_time(sec, what):
    beijing_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return beijing_time.timetuple()

logging.Formatter.converter = _beijing_time

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOG = logging.getLogger('taskbox')


def run_cmd(cmd_str):
    '''Run cmdline with shell'''

    out_err = subprocess.Popen(cmd_str, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    res = []
    for val in out_err:
        res.append(val.decode().replace('\\n', '\n'))
    return res


def auth_protect(func):
    '''Protect a route that need auth

    if the method is not GET, the auth is needed
    '''
    def wrap(req):
        if req.method != 'GET' and not req.is_authed:
            req.msg = ('danger', '该操作需要登录')
            # Error msg shown in 404.html
            return req.make_resp()
        return func(req)
    return wrap
