#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

from module import index
from module import post
from module import reply

######################
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# このやり方は気に入らない人がいるかも
db_uri = os.environ.get('DATABASE_URL') or "postgresql:///flasknote"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# FSADeprecationWarning を消すため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# モデル作成
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)

    def __init__(self, user_name):
        self.user_name = user_name

    def __repr__(self):
        return '<User %r>' % self.user_name
######################


# 投稿する
@app.route('/')
def do_index():
    do = index.Index()
    return render_template('index.html')

# 投稿結果
# 普通の投稿
@app.route('/post')
def do_post():
    do = post.Posts()
    return render_template('post.html', post_text=do.post_twitter())
# リプライ
@app.route('/reply', methods=['GET','POST'])
def do_reply():
    do = reply.Reply()
    if request.method == 'POST':
        result = request.form
    reply_name = result["reply_name"] 
    return render_template('post.html',post_text=do.send_reply(reply_name))

##########################
# ユーザー登録
@app.route('/register', methods=['GET','POST'])
def do_register():
    if request.method == 'POST':
        user_name= request.form['user_name']
    # ユーザー追加
    reg = User(user_name)
    db.session.add(reg)
    db.session.commit()
    return render_template('register.html')

##########################
"""
@app.route('/hello/<name>')
def hello(name=''):
    if name == '':
        name = u'ななしさん'
    return render_template('hello.html', name=name)
"""

@app.route('/debug')
def debug():
    return render_template('notemplate.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)

# 以上
