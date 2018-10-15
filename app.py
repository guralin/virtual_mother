#!/bin/env python
# coding: utf-8

import os
from flask import Flask, render_template
from datetime import datetime

import twitter

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
     
    api = twitter.Api(consumer_key="U84inIJFauv3RUFedHOwzPGLs",
        consumer_secret="VtbtEHaQz2hV3CTachsa29R4JOsLbVkTpxUoTbuSaPmSm5vhOa",
        access_token_key="1049129656379535360-LkXoFhHwr56IEH4TKS0LiE1sTK6VOj",
        access_token_secret="epwTxvBOiqijuDyeuyBdsRk8KyY8JA8PzGpVOD6jLRBIv"
        )
    api.PostUpdate("Flaskから3回めの投稿" + str(datetime.now()))

    return render_template('result.html')

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
