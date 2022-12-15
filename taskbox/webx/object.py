from base64 import b64decode
from functools import lru_cache
import time
import urllib.parse

from jinja2 import PackageLoader, Environment

from taskbox.webx import (
    route_auth,
    route_cmd,
    route_task,
    route_db,
    route_static,
)
from taskbox.taskbase import task


ROUTE = {
    # '': root path
    '': route_task.get_task,
    'task': route_task.get_task,
    'db': route_db.route,
    'cmd': route_cmd.cmdhandler,
    'static': route_static.render_static_html,
    'auth': route_auth.auth,
}
# One app instance may call muti req, so we asign global var here for muti uses.
HTML_ENV = Environment(loader=PackageLoader('taskdb.webx', 'templates'))


class Request():
    def __init__(self, event, context) -> None:
        '''Request instance

        Due to performace concern, better not connect db in here.
        '''
        self.starttime = time.perf_counter()
        httpinfo = event.get('requestContext').get('http')
        self.httpinfo = httpinfo
        self.method = httpinfo.get('method') # 'POST' ...
        self.path = httpinfo.get('path')
        self.useragent = httpinfo.get('userAgent')
        self.event = event
        self.context = context
        self.body = self._get_body()
        self.path_list = self._get_path_list()
        self.is_authed = _check_ip_is_authed(httpinfo['sourceIp'])
        # req.msg: {'type':success,info,warning,danger, 'info': any}

    def make_resp(self, http_code=200, template_name=None, **content_kw):
        '''response with html if the req is not from curl cmd

        content_kw: is a dict which is just what we return to curl cmd.
        TODO: need a json key for aws server to read. (implement set-cookie)
        '''
        if 'curl' in self.useragent:
            return content_kw
        else:
            self.timecost = round(time.perf_counter() - self.starttime, 6)
            return Request._resp_html(http_code=http_code,
                                      template_name=template_name,
                                      req=self, **content_kw)

    def _get_path_list(self):
        # from event get http info
        # path = [''] or ['path', 'to', 'smt']
        path = self.path.strip('/').split('/')
        return path

    def _get_body(self):
        res = None
        if self.method == 'POST':
            res = b64decode(self.event.get('body')).decode()
            # replace @ { } ...
            res = urllib.parse.unquote(res).replace('+', ' ')
        return res

    @staticmethod
    def _resp_html(http_code=200, template_name=None, **content_kw):
        body = HTML_ENV.get_template(template_name).render(**content_kw)
        return {
            "isBase64Encoded": False,
            "statusCode": http_code,
            "headers": {"Content-Type": "text/html"},
            "body": body if body else "Body is None",
        }

    def route(self):
        try:
            return ROUTE[self.path_list[0]](self)
        except KeyError:
            return 'no such route'

    def __str__(self) -> str:
        return f'Request: {self.method} {self.path}, body: {self.body}'

    def do_auth_login(self):
        app_context = task.get_app_db().get({'id': 'app_context'})
        if not app_context:
            app_context = {'id': 'app_context', 'cur_authed_srip': []}
        app_context.get('cur_authed_srip').append(self.httpinfo['sourceIp'])
        _check_ip_is_authed.cache_clear()
        task.get_app_db().update(app_context)

    def do_auth_logout(self):
        app_context = task.get_app_db().get({'id': 'app_context'})
        app_context.get('cur_authed_srip').remove(self.httpinfo['sourceIp'])
        _check_ip_is_authed.cache_clear()
        task.get_app_db().update(app_context)

    def __del__(self):
        '''Del method

        Excute some db write operate here after the wsgi response. So that
        the response works faster.💪
        '''
        pass


@lru_cache
def _check_ip_is_authed(ip_str):
    # {"id": "cur_authed_srip", "value": set()}
    app_context = task.get_app_db().get({'id': 'app_context'})
    if not app_context:
        # Got Typeerror if cur_authed_srip = {None, } here, So just asign a list
        app_context = {'id': 'app_context', 'cur_authed_srip': []}
        return False
    return ip_str in app_context.get('cur_authed_srip')

