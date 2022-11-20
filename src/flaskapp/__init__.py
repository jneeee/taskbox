import logging

from flask import Flask, render_template
from flask import jsonify
from flask import request

from src.utils.tools import run_cmd


LOG = logging.getLogger(__name__)

app = Flask(__name__, template_folder='src/flaskapp/templates')
app.debug = True


@app.route('/')
def wsgi_root():
    return jsonify('Coming soon!')


@app.route('/runcmd')
def cmdhandler():
    LOG.info(f"request.headers.cmd: {request.headers.get('cmd')}")
    cmd = request.headers.get('cmd')
    if not cmd:
        return jsonify('err: cmd is "None"!')

    res = run_cmd(cmd)
    LOG.info(f'run cmd: {cmd}, {res}')
    return jsonify(res)
