#!/bin/env python
# coding: utf-8

import os

from flask import Flask
app = Flask(__name__)
app.debug = True

from module import connect_twitter

#####データベース関連###############
from flask_sqlalchemy import SQLAlchemy

# テスト環境用の環境変数を読み込み、ない場合は本番環境として認識する
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')
# FSADeprecationWarning を消すため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Table(db.Model): # テーブルを指定
    __tablename__ = "morning_call_twitter"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)

class GetData(Table): # カラムの指定
    def __repr__(self):
        return self.user_name 
####################################

# データを取得
do = GetData # GetDataクラスの呼び出し
users = db.session.query(do).all()

# tweetする
post = connect_twitter.Twitter()
post.call(users)

