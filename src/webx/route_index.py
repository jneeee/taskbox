from json import dumps
import logging

from src.utils.tools import (
    run_cmd,
    get_http_header,
)

LOG = logging.getLogger(__name__)


def wsgi_root(*args):
    return 'Coming soon!\n'


def cmdhandler(event):
    http_info = get_http_header(event)
    cmd = http_info.get('cmd')
    if not cmd:
        return 'err: cmd is "None"!\n'

    res = run_cmd(cmd)
    print(f'run cmd: {cmd}, {res}')
    return res
