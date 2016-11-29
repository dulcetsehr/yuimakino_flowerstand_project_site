import json

server_types = ['dev', 'test', 'real']

with open('config.json', 'r') as f:
  CONFIG = json.loads(f.read().strip())

try:
  with open('SERVER_TYPE', 'r') as f:
    SERVER_TYPE = f.read().strip()
except:
  SERVER_TYPE = None

if SERVER_TYPE not in server_types: SERVER_TYPE = 'real'

print('Server Type: %s' % (SERVER_TYPE if SERVER_TYPE else 'real'))

CONFIG = CONFIG[SERVER_TYPE] if SERVER_TYPE in CONFIG else CONFIG['real']