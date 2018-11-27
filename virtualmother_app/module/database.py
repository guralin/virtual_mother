#!/bin/env python
# coding: utf-8

from virtualmother_app import db
from virtualmother_app.models import Table
from flask_sqlalchemy import SQLAlchemy



# views.py (/register)
class SendData(Table):
    # カラムに値を代入
    def __init__(self, user_id, get_up_time):
        self.user_id     = user_id
        self.get_up_time = get_up_time



class DBOperation():

    def __init__(self,db):
        self.db = db
    
    # 目覚ましの時間を新規登録
    def db_add(self, user_id, get_up_time):
        user_data = SendData(user_id, get_up_time)
        db.session.add(user_data)
        db.session.commit()


    # 目覚ましの時間の変更       ←※ 機能してません
    def update_get_up_time(self, user_id, get_up_time):
        user_data = db.session.query(Table).filter_by(user_id = f'{user_id}').first()
        print(user_data)
        user_data.get_up_time = f'{get_up_time}'
        db.session.add(user_data)
        db.session.commit()

    # 目覚まし解除
    def delete_get_up_time(self, user_id):
        user_data = db.session.query(Table).filter_by(user_id = f'{user_id}').first()
        db.session.delete(user_data)
        db.session.commit()



# morning.py
class GetData(Table): # カラムを指定してデータを取得
    def id_and_get_up(self):
        users = db.session.query(Table.user_id,Table.get_up_time).all()
        return users
    
    

    def __repr__(self):
        return self.user_id



