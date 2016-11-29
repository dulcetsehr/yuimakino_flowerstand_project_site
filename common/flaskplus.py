import os.path
from functools import wraps
from flask import Response, make_response, url_for

import common.helper


def make_url(endpoint, **kargs):
  res = url_for(endpoint, **kargs)
  if 'static' == endpoint:
    res += '?t=%d' % int(os.path.getmtime('.%s' % res))
  return res


def api_response(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    resp = make_response(f(*args, **kwargs))
    resp.headers['Cache-Control'] = 'no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp
  return decorated_function


def bson_response(f):
  @wraps(f)
  @api_response
  def decorated_function(*args, **kwargs):
    resp = f(*args, **kwargs)
    if type(resp) in [list, dict]:
      return Response(common.helper.bson_encode(resp), mimetype='text/plain;charset=utf-8')
    else:
      return resp
  return decorated_function


def json_response(f):
  @wraps(f)
  @api_response
  def decorated_function(*args, **kwargs):
    resp = f(*args, **kwargs)
    if type(resp) in [list, dict]:
      return Response(common.helper.json_encode(resp), mimetype='application/json;charset=utf-8')
    else:
      return resp
  return decorated_function


def text_response(f):
  @wraps(f)
  @api_response
  def decorated_function(*args, **kwargs):
    return Response(f(*args, **kwargs), mimetype='plain/text;charset=utf-8')
  return decorated_function






