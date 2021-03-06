#!/bin/env python
# coding: utf-8

# データベースのテーブルの指定

from virtualmother_app import db



class Table(db.Model): # テーブルの指定
    __tablename__ = "morning_call_user_data"
    user_index    = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.String(20), unique=True) # twitterID
    get_up_time   = db.Column(db.DateTime, nullable = True) # 起きてツイートする時間
    date          = db.Column(db.DateTime, nullable = True) # ユーザーが最後にDMのリンクをクリックした日付

class TodoTable(db.Model):
    __tablename__ = "user_todo_list"
    user_index    = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.String(20))
    todo         = db.Column(db.String(120), nullable = True) #朝連絡してほしいこと

    def __init__(self):
        db.create_all()
    # データベースを作るときは
    # ALTER TABLE morning_call_user_data ALTER get_up_time TYPE time without time zone;
    # を実行して、タイムゾーンを指定しなくても良いようにする



