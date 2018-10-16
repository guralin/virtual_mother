#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template
from datetime import datetime

import twitter

app = Flask(__name__)
app.debug = True

api = twitter.Api(consumer_key="U84inIJFauv3RUFedHOwzPGLs",
    consumer_secret="VtbtEHaQz2hV3CTachsa29R4JOsLbVkTpxUoTbuSaPmSm5vhOa",
    access_token_key="1049129656379535360-LkXoFhHwr56IEH4TKS0LiE1sTK6VOj",
    access_token_secret="epwTxvBOiqijuDyeuyBdsRk8KyY8JA8PzGpVOD6jLRBIv"
    )


# 投稿する
@app.route('/')
def index():
    return render_template('index.html')

# 投稿結果
@app.route('/post')
def post():
    post_text = "只今の時刻は「" + str(datetime.now()) + "」です (^_^)/"
    api.PostUpdate(post_text)
    return render_template('result.html',post_text=post_text)


@app.route('/hello/<name>')
def hello(name=''):
    if name == '':
        name = u'ななしさん'
    return render_template('hello.html', name=name)


@app.route('/debug')
def debug():
    return render_template('notemplate.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)

# end
