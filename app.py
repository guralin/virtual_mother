#!/bin/env python
# coding: utf-8

import os

from flask import Flask, render_template
app = Flask(__name__)
app.debug = True

from index import Index
from post import Post


# 投稿する
@app.route('/')
def index_do():
    do = Index()
    return render_template('index.html')

# 投稿結果
@app.route('/post')
def post_do():
    do = Post()
    return render_template('post.html', post_text=do.post_text())

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
