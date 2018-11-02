#!/bin/env python
# coding: utf-8

import os

from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

from module import twitter

#####################################
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

    def __init__(self, user_name):
        self.user_name = user_name
#####################################


# index
@app.route('/')
def do_index():
    return render_template('index.html')

# 投稿
@app.route('/post')
def do_post():
    do = twitter.Posts()
    post_text = do.post()
    return render_template('post.html', post_text=post_text)

# リプライ
@app.route('/reply', methods=['POST'])
def do_reply():
    reply_name = request.form["reply_name"] # index.htmlのフォームから取得
    do = twitter.Replies()
    post_text = do.reply(reply_name)
    return render_template('post.html',post_text=post_text)

# ユーザー登録
@app.route('/register', methods=['POST'])
def do_register():
    user_name = request.form['user_name'] # index.htmlのフォームから取得
    do = Register(user_name)
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



