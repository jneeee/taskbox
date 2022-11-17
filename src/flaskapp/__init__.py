from flask import Flask, render_template
from flask import jsonify
from flask import request


def get_app():
    app = Flask(__name__)
    app.debug = True
