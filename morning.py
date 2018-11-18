#!/bin/env python
# coding: utf-8

import os

from flask import Flask
from module import tweet
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

#####データベース関連###############
# テスト環境用の環境変数を読み込み、ない場合は本番環境として認識する
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')
# FSADeprecationWarning を消すため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Table(db.Model): # テーブルを指定
    __tablename__ = "morning_call_twitter"
    user_id = db.Column(db.Integer, primary_key=True) ### user_idをuser_indexに変更
    user_name = db.Column(db.String(80), unique=True) ### user_nameをuser_idに変更

class GetData(Table): # カラムの指定
    def __repr__(self):
        return self.user_name ### user_nameをuser_idに変更
####################################

# データを取得
do = GetData # GetDataクラスの呼び出し
###（追加） user_idを使って、スクリーン名を取得して、user_nameに格納
users = db.session.query(do).all() ###（変更）doをuser_nameに変更

# tweetする
post = tweet.Twitter()
post.call(users)

