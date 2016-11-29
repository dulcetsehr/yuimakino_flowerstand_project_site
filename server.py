# start server
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import common.flaskplus
import common.helper
from common.config import CONFIG, SERVER_TYPE


app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG['SESSION_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['RDB_CONNECTION_STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.db = SQLAlchemy(app)

import db

app.jinja_env.globals.update(make_url=common.flaskplus.make_url)
app.jinja_env.globals.update(min=min)
app.jinja_env.globals.update(max=max)
app.jinja_env.filters['json'] = common.helper.json_encode
app.jinja_env.filters['nl2br'] = common.helper.nl2br
app.jinja_env.filters['autolink'] = common.helper.make_autolink
app.jinja_env.filters['number'] = common.helper.number_format

from controllers.web import *

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=CONFIG['FLASK_PORT'], debug=CONFIG['DEBUG'])