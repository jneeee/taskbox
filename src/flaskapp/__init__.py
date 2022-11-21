import logging

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

from src.utils.tools import run_cmd


root_path = Blueprint('/', __name__)
LOG = logging.getLogger(__name__)


@root_path.route('/')
def wsgi_root():
    return jsonify('Coming soon!')


@root_path.route('/runcmd')
def cmdhandler():
    LOG.info(f"request.headers.cmd: {request.headers.get('cmd')}")
    cmd = request.headers.get('cmd')
    if not cmd:
        return jsonify('err: cmd is "None"!')

    res = run_cmd(cmd)
    LOG.info(f'run cmd: {cmd}, {res}')
    return jsonify(res)
