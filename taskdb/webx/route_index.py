from taskdb.utils.tools import (
    LOG,
    run_cmd,
    get_http_header,
)


def wsgi_root(*args):
    return args


def cmdhandler(event):
    http_info = get_http_header(event)
    cmd = http_info.get('cmd')
    if not cmd:
        res = 'err: cmd is "None"!\n'

    res = run_cmd(cmd)
    LOG.info(f'Run cmd: {cmd}, {res}')
    return res
