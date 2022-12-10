from base64 import b64decode
import urllib.parse

from jinja2 import PackageLoader, Environment

from src.webx import (
    route_index,
    route_task,
    route_db,
    route_static,
    route_user,
)
from src.task import models


ROUTE = {
    'task': route_task.get_task,
    'db': route_db.route,
    'cmd': route_index.cmdhandler,
    'static': route_static.render_static_html,
    'auth': route_user.auth,
}
HTML_ENV = Environment(loader=PackageLoader('src.webx', 'templates'))


class Request():
    def __init__(self, event) -> None:
        httpinfo = event.get('requestContext').get('http')
        self.httpinfo = httpinfo
        self.method = httpinfo.get('method') # 'POST' ...
        self.path = httpinfo.get('path')
        self.useragent = httpinfo.get('userAgent')
        self.event = event
        self.body = self._get_body()
        self.path_list = self._get_path_list()
        self.is_authed = self.check_is_authed()
        # req.msg: {'type':success,info,warning,danger, 'info': any}

    def make_resp(self, http_code=200, template_name=None, **content_kw):
        if 'curl' in self.useragent:
            return content_kw
        else:
            return Request._resp_html(http_code=http_code,
                                      template_name=template_name,
                                      req=self, **content_kw)

    def _get_path_list(self):
        # from event get http info
        # path = ['path', 'to', 'smt']
        try:
            path = self.path.strip('/').split('/')
        except KeyError:
            path = []
        return path if path[0] != '' else []

    def _get_body(self):
        res = None
        if self.method == 'POST':
            res = b64decode(self.event.get('body')).decode()
            # replace @ { } ...
            res = urllib.parse.unquote(res).replace('+', '')
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
        if not self.path_list:
            return route_index.wsgi_root(self)
        return ROUTE[self.path_list[0]](self)

    def __str__(self) -> str:
        return f'Request: {self.method} {self.path}, body: {self.body}'

    def check_is_authed(self):
        # {"id": "cur_authed_srip", "value": set()}
        app_context = models.get_app_db().get({'id': 'app_context'})
        if not app_context:
            # Got Typeerror if cur_authed_srip = {None, } here, So just asign a list
            app_context = {'id': 'app_context', 'cur_authed_srip': []}
            return False
        return self.httpinfo['sourceIp'] in app_context.get('cur_authed_srip')

    def do_auth_login(self):
        app_context = models.get_app_db().get({'id': 'app_context'})
        app_context.get('cur_authed_srip').append(self.httpinfo['sourceIp'])
        models.get_app_db().update(app_context)

    def do_auth_logout(self):
        app_context = models.get_app_db().get({'id': 'app_context'})
        app_context.get('cur_authed_srip').remove(self.httpinfo['sourceIp'])
        models.get_app_db().update(app_context)
