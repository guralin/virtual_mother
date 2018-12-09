#!/bin/env python
# coding: utf-8

from virtualmother_app import db
from virtualmother_app.models import Table
from flask_sqlalchemy import SQLAlchemy
import datetime


# views.py (/register)
class SendData(Table):
    # カラムに値を代入
    def __init__(self, user_id, get_up_time):
        self.user_id     = user_id
        self.get_up_time = get_up_time



class SendDate(Table):
    def __init__(self, user_id, date):
        self.user_id = user_id
        self.date    = date



class DBOperation():

    def __init__(self,db):
        self.db = db
    
    # 目覚ましの時間を新規登録
    def insert_get_up_time(self, user_id, get_up_time):
        user_data = SendData(user_id, get_up_time)
        db.session.add(user_data)
        db.session.commit()

    # 日付を登録
    def insert_date(self, user_id):
        user_data = SendDate(user_id, datetime.date.today())
        db.session.add(user_data)
        db.session.commit()

    # 目覚ましの時間の変更       
    def update_get_up_time(self, user_id, get_up_time):
        user_data = db.session.query(Table).filter(Table.user_id == user_id).first()
        user_data.get_up_time = get_up_time
        db.session.commit()

    # 日付の更新（DMのリンクをクリックした時）
    def update_date(self, user_id):
        user_data = db.session.query(Table).filter(Table.user_id == user_id).first()
        user_data.date = datetime.date.today() #(1600, 2, 4)
        print(user_data.date)
        db.session.commit()

    # 目覚まし解除
    def delete_get_up_time(self, user_id):
        user_data = db.session.query(Table).filter(Table.user_id == user_id).first()
        user_data.get_up_time = None
        db.session.commit()



# morning.py
class GetData(Table): # カラムを指定してデータを取得
    def id_and_get_up(self):
        users_data = db.session.query(Table.user_id, Table.get_up_time, Table.date).all()
        return users_data
    


