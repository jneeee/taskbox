import subprocess
import logging


LOG = logging.getLogger('taskdb')
LOG.setLevel(logging.INFO)

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
