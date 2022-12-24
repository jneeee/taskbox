from base64 import b64decode
from functools import lru_cache
import traceback
import time
import urllib.parse
from uuid import uuid4

from jinja2 import PackageLoader, Environment

from taskbox.webx import (
    route_auth,
    route_cmd,
    route_task,
    route_db,
    route_static,
)
from taskbox.taskbase import task
from taskbox.utils.tools import LOG


ROUTE = {
    # '': root path
    '': route_task.get_task,
    'task': route_task.get_task,
    'db': route_db.route,
    'cmd': route_cmd.cmdhandler,
    'static': route_static.render_static_html,
    'auth': route_auth.auth,
}
# One app instance may call multi req, so we asign global var here for muti uses.
HTML_ENV = Environment(loader=PackageLoader('taskbox.webx', 'templates'))


class Request():
    def __init__(self, event, context) -> None:
        '''Request instance

        Due to performace concern, better not connect db in here.
        '''
        self.starttime = time.perf_counter()
        httpinfo = event.get('requestContext', {}).get('http', {})
        self.httpinfo = httpinfo
        self.method = httpinfo.get('method') # 'POST' ...
        self.path = httpinfo.get('path')
        self.useragent = httpinfo.get('userAgent')
        self.event = event
        self.context = context
        self.body = self._get_body()
        self.path_list = self._get_path_list()

        self.headers = event.get('headers')
        self.uuid = self._get_cookies_uuid()
        self.is_authed = \
            _check_authid_is_valid(self.uuid)
        self.resp_headers = {"Content-Type": "text/html"}
        LOG.info(f'Request: {self.__dict__}')

    def make_resp(self, http_code=200, template_name='404.html', **content_kw):
        '''response with html if the req is not from curl cmd

        content_kw: is a dict which is just what we return to curl cmd.
        '''
        self.timecost = round((time.perf_counter()-self.starttime)*1000, 2)
        content_kw['req'] = self
        body = HTML_ENV.get_template(template_name).render(**content_kw)
        return {
            "isBase64Encoded": False,
            "statusCode": http_code,
            "headers": self.resp_headers,
            "body": body if body else "Body is None",
        }

    def _get_cookies_uuid(self):
        '''Get cookie uuid from req

        uuid is for session manage
        :return: None or uuid str
        '''
        cookies = self.event.get('cookies')
        if not isinstance(cookies, list):
            return None
        uuid = None
        for coo_str in cookies:
            # coo_str = 'uuid=<uuid>'
            if coo_str.startswith('uuid'):
                _, uuid = coo_str.split('=')
                break
        return uuid

    def _get_path_list(self):
        # from event get http info
        # path = [''] or ['path', 'to', 'smt']
        path = self.path.strip('/').split('/')
        return path

    def _get_body(self):
        '''Return a dict'''
        res = None
        if self.method == 'POST':
            res = b64decode(self.event.get('body')).decode()
            # replace @ { } ...
            res = urllib.parse.unquote(res).replace('+', ' ')
            res = {k: v for k,v in map(lambda kv: kv.split('=', 1), res.split('&'))}
        return res

    def route(self):
        try:
            return ROUTE[self.path_list[0]](self)
        except KeyError as e:
            LOG.exception(e)
            self.msg = ('danger', traceback.format_exc())
            return self.make_resp(http_code=404)

    def __str__(self) -> str:
        return f'Request: {self.method} {self.path}, body: {self.body}'

    def do_auth_login(self):
        app_context = task.Task.get_tb().get({'id': 'app_context', 'name':'app'})
        if not app_context:
            app_context = {'id': 'app_context', 'name':'app', 'cur_authids': {}}
        uuid = str(uuid4())
        # expire after 24 hours
        expire_at = int(time.time()) + 86400
        if 'cur_authids' not in app_context:
            app_context['cur_authids'] = {}
        app_context['cur_authids'][uuid] = {'expire_at': expire_at}
        self.resp_headers['Set-Cookie'] = f'uuid={uuid}; Max-Age=86400; path=/'
        _check_authid_is_valid.cache_clear()
        task.Task.get_tb().put(app_context)

    def do_auth_logout(self):
        app_context = task.Task.get_tb().get({'id': 'app_context', 'name':'app'})
        try:
            app_context['cur_authids'].pop(self.uuid)
        except KeyError:
            pass
        _check_authid_is_valid.cache_clear()
        self.resp_headers['Set-Cookie'] = f'uuid={self.uuid}; Max-Age=-1; path=/'

        task.Task.get_tb().put(app_context)

    def __del__(self):
        '''Del method

        Excute some db write operate here after the wsgi response. So that
        the response works faster.💪
        '''
        pass


@lru_cache
def _check_authid_is_valid(uuid):
    # app_context = {'id': 'app_context', 'name':'app', 'cur_authids':
    # {<uuid>: {expire_at: <int>},}}
    if not uuid:
        return False
    tb = task.Task.get_tb()
    app_context = tb.get({'id': 'app_context', 'name':'app'})
    if not app_context:
        return False

    cur_time = int(time.time())
    new_authids = {}
    for uuid, prop in app_context.get('cur_authids', {}).items():
        if prop.get('expire_at') < cur_time:
            continue
        else:
            new_authids[uuid] = prop

    app_context['cur_authids'] = new_authids
    tb.put(app_context)
    LOG.info(f'new_authids: {new_authids}')
    return uuid in new_authids
