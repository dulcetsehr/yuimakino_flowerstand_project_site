import datetime
import types

from server import app

class Contact(app.db.Model):
  __tablename__ = 'ym201701_contacts'
  
  idx = app.db.Column(app.db.BigInteger, primary_key=True)
  nickname = app.db.Column(app.db.Text, nullable=False)
  boardname = app.db.Column(app.db.Text, nullable=False)
  bankname = app.db.Column(app.db.Text, nullable=False)
  price = app.db.Column(app.db.Integer, nullable=False, default=0)
  contact_number = app.db.Column(app.db.Text, nullable=False)
  password = app.db.Column(app.db.Text, nullable=False)
  visible = app.db.Column(app.db.Boolean, nullable=False, default=True)
  
  reg_dt = app.db.Column(app.db.DateTime, nullable=False)
  upd_dt = app.db.Column(app.db.DateTime)
  
  check_price = app.db.Column(app.db.Integer, nullable=False, default=0)
  
  def to_dict(self):
    return {n: getattr(self, n).isoformat() if type(getattr(self, n))in[datetime.datetime, datetime.date, datetime.time] else getattr(self, n) for n in dir(self) if n[0] != '_' and n[0:5] != 'query' and n != 'metadata' and type(getattr(self,n)) not in [staticmethod, types.FunctionType, types.MethodType]}


class Message(app.db.Model):
  __tablename__ = 'ym201701_messages'
  
  idx = app.db.Column(app.db.BigInteger, primary_key=True)
  nickname = app.db.Column(app.db.Text, nullable=False)
  boardname = app.db.Column(app.db.Text, nullable=False)
  message = app.db.Column(app.db.Text, nullable=False)
  password = app.db.Column(app.db.Text, nullable=False)
  visible = app.db.Column(app.db.Boolean, nullable=False, default=True)
  
  reg_dt = app.db.Column(app.db.DateTime, nullable=False)
  upd_dt = app.db.Column(app.db.DateTime)
  
  def to_dict(self):
    return {n: getattr(self, n).isoformat() if type(getattr(self, n))in[datetime.datetime, datetime.date, datetime.time] else getattr(self, n) for n in dir(self) if n[0] != '_' and n[0:5] != 'query' and n != 'metadata' and type(getattr(self,n)) not in [staticmethod, types.FunctionType, types.MethodType]}

