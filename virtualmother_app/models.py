#!/bin/env python
# coding: utf-8

# データベースのテーブルの指定



from virtualmother_app import db



class Table(db.Model): # テーブルの指定
    __tablename__ = "morning_call_user_data"
    user_index    = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.String(20), unique=True) # twitterID
    get_up_time   = db.Column(db.DateTime) # 起きてツイートする時間

def init():
    db.create_all()



