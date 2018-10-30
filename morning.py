#!/bin/env python
# coding: utf-8

import os

from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

# ===Twitter関連===
import twitter
from datetime import datetime
api = twitter.Api(consumer_key= os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
    )

# ===データベース関連===
import psycopg2
from flask_sqlalchemy import SQLAlchemy
# このやり方は気に入らない人がいるかも
db_uri = os.environ.get('DATABASE_URL') or "postgresql:///flasknote"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# FSADeprecationWarning を消すため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# モデル
class Register(db.Model):
    __tablename__ = "morning_call_twitter"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<User %r>' % self.user_name


# 「@~　起きて！！！　「〜時〜分」だよ」とTwitterに投稿する
do = Register
users = db.session.query(do).all()

for user in users:
    user = str(user).split("'")
    user = user[1]
    morning_call = "@{0}\n起きて！\n「{1} 」だよ！！！".format(user,datetime.now())
    api.PostUpdate(morning_call)
    print(user)



