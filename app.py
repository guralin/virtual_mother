#!/bin/env python
# coding: utf-8

import os, sys
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

from module import index
from module import post
from module import reply

######################
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# モデル作成
class User(db.Model):
    __tablename__ = 'morning_call_twitter'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True)

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
@app.route('/reply', methods=['POST'])
def do_reply():
    do = reply.Reply()
    if request.method == 'POST':
        result = request.form["reply_name"]
    reply_name = result 
    return render_template('post.html',post_text=do.send_reply(reply_name))

##########################
# ユーザー登録
@app.route('/register', methods=['POST'])
def do_register():
    if request.method == 'POST':
        user_name = request.form['user_name']
    # ユーザー追加
    __tablename__ = 'morning_call_twitter'
    reg = User(user_name)
    db.session.add(reg)
    try:
        db.session.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    return render_template('register.html',user_name=user_name)

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
