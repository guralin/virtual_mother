#!/bin/env python
# coding: utf-8

import os

from flask import Flask
app = Flask(__name__)
app.debug = True

from module import twitter

#####データベース関連###############
from flask_sqlalchemy import SQLAlchemy

# テスト環境用の環境変数を読み込み、ない場合は本番環境として認識する
db_uri = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# FSADeprecationWarning を消すため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# モデル
class Register(db.Model):
    __tablename__ = "morning_call_twitter"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)

    def __repr__(self): #←必要だった(読み出す時？)
        return '<User %r>' % self.user_name
####################################

# データを取得
do = Register
users = db.session.query(do).all()

# tweetする
post = twitter.MorningCalls()
post.call(users)

