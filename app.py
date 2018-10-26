#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

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
