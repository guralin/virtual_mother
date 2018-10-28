#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, request,g
app = Flask(__name__)
app.debug = True
import sqlite3

from module import index
from module import post


# 投稿する
@app.route('/')
def index_do():
    do = index.Index()
    return render_template('index.html')

# 投稿結果
@app.route('/post')
def post_do():
    do = post.Posts()
    return render_template('post.html', post_text=do.twitter_upload())

@app.route('/reply', methods=['GET','POST'])
def do_post_reply():
    do = post.Posts()
    if request.method == 'POST':
        result = request.form
    reply_name = result["reply_name"] 
    post_text = do.send_reply(reply_name)
    return render_template('post.html',post_text=post_text)

@app.route('/dbtest')
def hello_world():
    entries =get_db().execute('select title, body from entries').fetchall()
    return render_template('dbtest.html', entries=entries)


# Database
def connect_db():
    db_path = os.path.join(app.root_path, 'flasknote.db')
    rv = sqlite3.connect(db_path)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

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
