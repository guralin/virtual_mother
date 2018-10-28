#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, request,g, redirect, url_for
app = Flask(__name__)
app.debug = True
from flask_sqlalchemy import SQLAlchemy

from module import index
from module import post


db_uri = os.environ.get('DATABASE_URL') or "postgresql:///flasknote"# 追加
#db_uri = "postgresql:///flasknote"# 追加
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri # 追加
db = SQLAlchemy(app) # 追加


class Entry(db.Model): # 追加
    __tablename__ = "entries" # 追加
    id = db.Column(db.Integer, primary_key=True) # 追加
    title = db.Column(db.String(), nullable=False) # 追加
    body = db.Column(db.String(), nullable=False) # 追加


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
    entries = Entry.query.all()
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

@app.route('/dbpost', methods=['POST'])
def add_entry():
    entry = Entry()
    entry.title = request.form['title']
    entry.body = request.form['body']
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('hello_world'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)

# 以上
