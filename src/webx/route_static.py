from src.utils.tools import LOG


def render_static_html(req):
    if len(req.path_list) < 1:
        raise ValueError(f'Invalid static html path: {req.path_list}')
    else:
        return req.make_resp(template_name=req.path_list[1])
