import subprocess
from jinja2 import PackageLoader, Environment


def run_cmd(cmd_str):
    res = b''
    out, err = subprocess.Popen(cmd_str, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    if out:
        res = out
    else:
        res = err
    return res.decode().replace('\\n', '\n')

def get_http_path(event):
    # from event get http info
    # path = ['path', 'to', 'smt']
    try:
        tmp = event['requestContext']['http']
        path = tmp['path'].strip('/').split('/')
    except KeyError:
        path = []
    return path if path[0] != '' else []


def get_http_header(event):
    try:
        info = event['headers']
    except KeyError:
        info = {}
    return info


def _template_render(body, template_name=None):
    env = Environment(loader=PackageLoader('src.webx', 'templates'))
    template = env.get_template(template_name)
    return template.render(tasks_list=body)


def resp_html(body, http_code=200, template_name=None):
    body = _template_render(body, template_name=template_name)
    return {
        "isBase64Encoded": False,
        "statusCode": http_code,
        "headers": {"Content-Type": "text/html"},
        "body": body if body else "Body is None",
    }
