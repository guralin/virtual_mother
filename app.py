#!/bin/env python
# coding: utf-8

import os
import logging

import oauth2 as oauth

from flask import Flask, render_template, request, jsonify
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

# oauth関連#######################
request_token_url = 'https://twitter.com/oauth/request_token'
access_token_url  = 'https://twitter.com/oauth/access_token'
authenticate_url  = 'https://twitter.com/oauth/authorize'
callback_url      = 'https://virtualmother-develop.herokuapp.com/authorize'# テスト環境用
#callback_url      = 'https://oauth-test-virtualmother.herokuapp.com/'# テスト環境用
consumer_key      = os.environ.get("CONSUMER_KEY")  # 各自設定する
consumer_secret   = os.environ.get("CONSUMER_SECRET") # 各自設定する
#################################
# todo 分析できたら別モジュールに移植しましょう
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

def get_request_token():
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    resp, content = client.request('%s?&oauth_callback=%s' % (request_token_url, callback_url))
    content = content.decode('utf-8')
    request_token = dict(parse_qsl(content))
    return request_token['oauth_token']

#成型
def parse_qsl(url):
    param = {}
    try:
        for i in url.split('&'):
            _p = i.split('=')
            param.update({_p[0]: _p[1]})
    except:
        param['oauth_token'] ='failed'
        param['oauth_token_secret'] ='failed'
    return param

#アクセストークンを取得する関数
def get_access_token(oauth_token, oauth_verifier):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(oauth_token, oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request("https://api.twitter.com/oauth/access_token","POST", body="oauth_verifier={0}".format(oauth_verifier))
    return content
###############################


# index
@app.route('/')
def do_index():
    return render_template('index.html')

# oauth
@app.route("/authorize")
def check_token():
    oauth_token = request.args.get('oauth_token', default = "failed", type = str)
    oauth_verifier = request.args.get('oauth_verifier', default = "failed", type = str)

    if oauth_token != "failed" and oauth_verifier !="failed":
        logging.debug("oauth_token and oauth_verifier is not failed")
        response = get_access_token(oauth_token, oauth_verifier).decode('utf-8')
        response = dict(parse_qsl(response))
        oauth_token = response['oauth_token']
        oauth_token_secret = response['oauth_token_secret']
        return render_template('cer.html',url="NoNeed",oauth_token=oauth_token,oauth_token_secret=oauth_token_secret)
    else:
        logging.debug("oauth_token or oauth_verifier is failed")
        #リクエストトークンを取得する
        request_token = get_request_token()
        authorize_url = '%s?oauth_token=%s' % (authenticate_url, request_token)
        logging.debug(authorize_url)
        return render_template('cer.html',url=authorize_url,res="NoParams")


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


# 404ページ
#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template(page_not_found.html, 404)



