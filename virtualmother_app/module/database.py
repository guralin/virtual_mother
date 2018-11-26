#!/bin/env python
# coding: utf-8

from virtualmother_app import db
from virtualmother_app.models import Table



# views.py (/register)
class SendData(Table): # カラムに値を代入

    def __init__(self, user_id, get_up_time):
        self.user_id     = user_id
        self.get_up_time = get_up_time



class DBOperation():

    def __init__(self,db):
        self.db = db
    

    def db_add(self, user_id, get_up_time):
        do = SendData(user_id, get_up_time)
        db.session.add(do)
        db.session.commit()


# 一致するユーザー
    def update_get_up_time(self, user_id,get_up_time):
        do = db.session.query(Table).filter(Table.user_id==user_id).first()
        do.get_up_time = get_up_time
        db.session.commit()

# morning.py
class GetData(Table): # カラムを指定してデータを取得
    def id_and_get_up(self):
        users = db.session.query(Table.user_id,Table.get_up_time).all()
        return users
    
    

    def __repr__(self):
        return self.user_id



