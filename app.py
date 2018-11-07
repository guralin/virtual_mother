#!/bin/env python
# coding: utf-8

import os

from module import tweet
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

#####データベース関連###############


# テスト環境用の環境変数を読み込み、ない場合は本番環境として認識する
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')
# FSADeprecationWarning を消すため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Table(db.Model): # テーブルの指定
    __tablename__ = "morning_call_twitter"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)

class SendData(Table): # カラムに値を代入
    def __init__(self, user_name):
        self.user_name = user_name
###################################


# index
@app.route('/')
def do_index():
    return render_template('index.html')

# ユーザー
@app.route('/user')
def do_user():
    return render_template('user.html')

# 投稿
@app.route('/post')
def do_post():
    do = tweet.Twitter()
    post_text = do.post()
    return render_template('post.html', post_text=post_text)

# リプライ
@app.route('/reply', methods=['POST'])
def do_reply():
    reply_name = request.form["reply_name"] # index.htmlのフォームから取得
    do = tweet.Twitter()
    post_text = do.reply(reply_name)
    return render_template('post.html',post_text=post_text)

# ユーザー登録
@app.route('/register', methods=['POST'])
def do_register():
    user_name = request.form['user_name'] # index.htmlのフォームから取得
    do = SendData(user_name)
    db.session.add(do)
    db.session.commit()
    return render_template('register.html',user_name=user_name)


# デバッグ
@app.route('/debug')
def debug():
    return render_template('notemplate.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)



