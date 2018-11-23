#!/bin/env python
# coding: utf-8

from datetime import time

from virtualmother_app import db
from virtualmother_app.models import Table



# views.py (/register)
class SendData(Table): # カラムに値を代入
    def __init__(self, user_id, get_up_time):
        self.user_id      = user_id
        self.get_up_time  = get_up_time

class DBOperation():
    def __init__(self,db):
        self.db = db
    
    def db_add(self, user_id, get_up_time=time(7,0)):
            do = SendData(user_id, get_up_time)
            db.session.add(do)
            db.session.commit()

# morning.py
class GetData(Table): # カラムを指定してデータを取得
    def __repr__(self):
        return self.user_id
