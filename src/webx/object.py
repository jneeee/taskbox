from base64 import b64decode

from jinja2 import PackageLoader, Environment

from src.webx import (
    route_index,
    route_task,
    route_db,
)

ROUTE = {
    'task': route_task.get_task,
    'db': route_db.route,
    'cmd': route_index.cmdhandler,
}
HTML_ENV = Environment(loader=PackageLoader('src.webx', 'templates'))


class Request():
    def __init__(self, event) -> None:
        httpinfo = event.get('requestContext').get('http')
        self.method = httpinfo.get('method') # 'POST' ...
        self.path = httpinfo.get('path')
        self.useragent = httpinfo.get('userAgent')
        self.event = event
        self.body = self._get_body()

    def make_resp(self, http_code=200, template_name=None, **content_kw):
        if 'curl' in self.useragent:
            return content_kw
        else:
            return Request._resp_html(http_code=http_code,
                                      template_name=template_name, **content_kw)

    @property
    def path_list(self):
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
        # import pdb;pdb.set_trace()
        if not self.path_list:
            return route_index.wsgi_root(self)
        return ROUTE[self.path_list[0]](self)

    def __str__(self) -> str:
        return f'Request: {self.method} {self.path}, body: {self.body}'

