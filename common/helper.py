import base64
import datetime
import hashlib
import hmac
import json
import math
import os.path
import random
import re
import string
import time
import traceback
from bson import BSON, json_util

from common.config import CONFIG


##########
# debug functions
##########
def trace_error(**kargs):
  lines = traceback.format_exc().strip().split('\n')
  nstr, rl, lines = '', [lines[-1]], lines[1:-1]
  lines.reverse()
  
  for i in range(len(lines)):
    line = lines[i].strip()
    if line.startswith('File "'):
      eles = line.split('"')
      basename, lastdir = os.path.basename(eles[1]), os.path.basename(os.path.dirname(eles[1]))
      eles[1] = '%s/%s' % (lastdir, basename)
      rl.append('^\t%s %s' % (nstr, '"'.join(eles)))
      nstr = ''
    else:
      nstr += line
  
  result = '----------\n%s\n----------' % '\n'.join(rl)
  if 'out' in kargs and kargs['out']: print(result)
  return result



##########
# encode / decode functions
##########
def json_encode(data, **kargs):
  try:
    return json.dumps(data, sort_keys=True, indent=0, default=json_util.default).replace('\n', '')
  except:
    return None

def json_decode(data, **kargs):
  try:
    if type(data) == bytes: data = data.decode('utf-8')
    return json.loads(data)
  except:
    trace_error(out=True)
    return None

# input: dict or array
# output: bytes if raw else str
def bson_encode(data, **kargs):
  try:
    return BSON.encode(data) if kargs.get('raw') else base_encode(BSON.encode(data))
  except:
    return None

# input: str or bytes
# output: dict or array
def bson_decode(data, **kargs):
  try:
    return BSON.decode(data) if kargs.get('raw') else BSON.decode(base_decode(data))
  except:
    trace_error(out=True)
    return None

def base_encode(msg):
  return base64_encode(msg)

def base_decode(msg):
  return base64_decode(msg)

def base64_encode(msg):
  return base64.b64encode(msg) if msg else None

def base64_decode(msg):
  return base64.b64decode(msg) if msg else None


##########
# validate functions
##########
def validate_alpha(value):
  regex = re.compile('[A-Za-z]+')
  return True if regex.search(value) else False

def validate_number(value):
  regex = re.compile('[0-9]+')
  return True if regex.search(value) else False

def validate_email(value):
  regex = re.compile('^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
  return True if regex.match(value) else False


##########
# hash functions
##########
# input: str or bytes
# output: str
def md5(data, **kargs):
  if not data: return None
  if type(data) == str: data = data.encode('utf-8') # str to bytes
  hm = hashlib.md5(data)
  if kargs.get('hex'): return hm.hexdigest()
  return hm.digest() if kargs.get('raw') else base_encode(hm.digest())

# input: str or bytes
# output: str
def sha1(data, **kargs):
  if not data: return None
  if type(data) == str: data = data.encode('utf-8') # str to bytes
  hm = hashlib.sha1(data)
  if kargs.get('hex'): return hm.hexdigest()
  return hm.digest() if kargs.get('raw') else base_encode(hm.digest())

# input: str or bytes
# output: str
def sha256(data, **kargs):
  if not data: return None
  if type(data) == str: data = data.encode('utf-8') # str to bytes
  hm = hashlib.sha256(data)
  if kargs.get('hex'): return hm.hexdigest()
  return hm.digest() if kargs.get('raw') else base_encode(hm.digest())

# input: str or bytes
# output: str
def hmac_md5(data, key=None, **kargs):
  if not data: return None
  if not key: key = CONFIG['SESSION_SECRET_KEY'] # default hmac key
  if type(data) == str: data = data.encode('utf-8') # str to bytes
  if type(key) == str: key = key.encode('utf-8') # str to bytes
  hm = hmac.new(key, data, hashlib.md5)
  if kargs.get('hex'): return hm.hexdigest()
  return hm.digest() if kargs.get('raw') else base_encode(hm.digest())

# input: str or bytes
# output: str
def hmac_sha1(data, key=None, **kargs):
  if not data: return None
  if not key: key = CONFIG['SESSION_SECRET_KEY'] # default hmac key
  if type(data) == str: data = data.encode('utf-8') # str to bytes
  if type(key) == str: key = key.encode('utf-8') # str to bytes
  hm = hmac.new(key, data, hashlib.sha1)
  if kargs.get('hex'): return hm.hexdigest()
  return hm.digest() if kargs.get('raw') else base_encode(hm.digest())

# input: str or bytes
# output: str
def hmac_sha256(data, key=None, **kargs):
  if not data: return None
  if not key: key = CONFIG['SESSION_SECRET_KEY'] # default hmac key
  if type(data) == str: data = data.encode('utf-8') # str to bytes
  if type(key) == str: key = key.encode('utf-8') # str to bytes
  hm = hmac.new(key, data, hashlib.sha256)
  if kargs.get('hex'): return hm.hexdigest()
  return hm.digest() if kargs.get('raw') else base_encode(hm.digest())

# input: str or bytes
# output: str
def hash_password(password):
  return hmac_sha1(password, CONFIG['SESSION_PASSWORD_SECRET_KEY'], hex=True) # use different secret key: for security



##########
# io functions
##########
def read_file(filepath, fallback=None, **kargs):
  data = fallback
  try:
    with open(filepath, 'r') as f:
      data = f.read().strip()
    if type(data) == str:
      data = data.decode('utf-8', 'ignore')
  except:
    data = fallback
  return string_replace(data, kargs) if data else None

##########
# util functions
##########
def rand(min=0, max=999999):
  random.seed()
  return random.randint(min, max)

def parseint(value, fallback=0):
  try:
    value = int(value)
  except:
    value = fallback
  return value

def parsefloat(value, fallback=0):
  try:
    value = float(value)
  except:
    value = fallback
  return value




##########
# string functions
##########
def nl2br(value):
  _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
  return u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>') for p in _paragraph_re.split(value))

def get_random_chars(size=12, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
  random.seed()
  return ''.join(random.choice(chars) for x in range(size))

def make_autolink(val):
  return re.sub(u'(https?://([-\w\.]+[-\w])+(:\d+)?(/([\w/_\.#-]*(\?\S+)?[^\.\s　])?)?)', r'<a href="\1" target="_blank">\1</a>', val)

def str_replace(val, target, **kargs):
  open, close = kargs.get('open') or '[', kargs.get('close') or ']'
  
  for key in target:
    #if type(key) == unicode: key = key.encode('utf8', 'ignore')
    try:
      #if type(target[key]) not in [str, unicode]: target[key] = unicode(target[key])
      if type(target[key]) != str: target[key] = str(target[key])
      val = val.replace('%s%s%s' % (open, key, close), target[key])
    except:
      pass
  return val

def number_format(val):
  return '{:,d}'.format(val)



##########
# datetime functions
##########
def get_today():
  return datetime.date.today()
def get_now():
  return datetime.datetime.now()

def get_timestamp(dt = get_now()):
  return parseint(dt.strftime('%s'))

def datetime_to_format(time):
  return time.strftime('%Y-%m-%d %H:%M:%S')

def timestamp_to_datetime(timestamp):
  return datetime.datetime.fromtimestamp(timestamp)


##########
# Email Functions
##########
## TODO

