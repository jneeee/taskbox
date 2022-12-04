import logging

from src.task import models
from src.utils import tools

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def route(event):
    path = tools.get_http_path(event)
    if len(path) == 1:
        return tools.resp_html(template_name='dynamodb.html')
    elif path[1] == 'quary':
        # quary_res = models.get_app_db().get({'id'})
        return tools.resp_html(quary_res=[event,], template_name='dynamodb.html')


def db_quary(event):
    pass
