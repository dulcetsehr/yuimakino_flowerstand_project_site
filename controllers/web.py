from flask import abort, request, render_template, session
from sqlalchemy import func

import common.helper
from common.flaskplus import json_response
from server import app

import db



@app.route('/', methods=['GET'])
def web_index():
  session.pop('edit_idx', None)
  
  return render_template('index.html')
  

@app.route('/process', methods=['POST'])
@json_response
def api_process():
  if request.host not in request.referrer: return abort(403)
  
  if not request.json.get('nickname'): return {'result': 1}
  if not request.json.get('boardname'): return {'result': 2}
  if not request.json.get('bankname'): return {'result': 3}
  if not request.json.get('price') or common.helper.parseint(request.json.get('price')) < 1: return {'result': 4}
  if not request.json.get('contact_number'): return {'result': 5}
  
  idx = common.helper.parseint(request.json.get('idx', '0'))
  if idx > 0 and session.get('edit_idx') != idx: return {'result': 7}
  
  obj = db.Contact.query.filter_by(idx=idx, visible=True).first()
  if not obj:
    if not request.json.get('password'): return {'result': 6}
    
    obj = db.Contact()
    obj.password = common.helper.hash_password(request.json.get('password'))
    obj.reg_dt = common.helper.get_now()
    app.db.session.add(obj)
  else:
    if request.json.get('password'): obj.password = common.helper.hash_password(request.json.get('password'))
    obj.upd_dt = common.helper.get_now()
    session.pop('edit_idx', None)
    
  obj.nickname = request.json.get('nickname')
  obj.boardname = request.json.get('boardname')
  obj.bankname = request.json.get('bankname')
  obj.price = common.helper.parseint(request.json.get('price'))
  obj.contact_number = request.json.get('contact_number')
  
  app.db.session.commit()
  
  return {'result': 0}



@app.route('/check', methods=['POST'])
@json_response
def api_check():
  if request.host not in request.referrer: return abort(403)
  
  session.pop('edit_idx', None)
  
  nickname = request.json.get('nickname')
  password = common.helper.hash_password(request.json.get('password'))
  
  obj = db.Contact.query.filter_by(nickname=nickname, password=password, visible=True).first()
  if obj:
    session['edit_idx'] = obj.idx
    obj = obj.to_dict()
    del obj['password'], obj['reg_dt'], obj['upd_dt'], obj['visible']
    return {'result': 0, 'data': obj}
  
  return {'result': 8}




@app.route('/leave/<int:idx>', methods=['DELETE'])
@json_response
def api_leave(idx):
  if request.host not in request.referrer: return abort(403)
  
  obj = db.Contact.query.filter_by(idx=idx, visible=True).first()
  if obj:
    obj.visible=False
    app.db.session.commit()
  
  return {'result': 0}
  


