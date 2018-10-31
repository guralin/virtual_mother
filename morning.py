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

# ###データベース関連###############
from flask_sqlalchemy import SQLAlchemy

db_uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# FSADeprecationWarning を消すため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# モデル
class Register(db.Model):
    __tablename__ = "morning_call_twitter"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)
####################################

# 「@~　起きて！！！　「〜時〜分」だよ」とTwitterに投稿する
do = Register
users = db.session.query(do).all()

for user in users:
    user = str(user).split("'")
    user = user[1]
    now_hour_and_minute = "{0:%H}時{0:%M}分".format(datetime.now())
    morning_call = "@{0}\n もう{1}よ！\n 起きなさい！".format(user,now_hour_and_minute)
    print(morning_call)
    api.PostUpdate(morning_call)



