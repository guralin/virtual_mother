#!/bin/env python
# coding: utf-8

import os
import logging

import oauth2 as oauth
from module import tweet

from flask import Flask, render_template, request, jsonify, redirect
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
    user_id = db.Column(db.Integer, primary_key=True) ###（変更）user_idをuser_indexに変更
    user_name = db.Column(db.String(80), unique=True) ###（変更）user_nameをuser_idに変更

class SendData(Table): # カラムに値を代入
    def __init__(self, user_name):
        self.user_name = user_name
###################################

# oauth関連#######################
request_token_url = 'https://twitter.com/oauth/request_token'
access_token_url  = 'https://twitter.com/oauth/access_token'
authenticate_url  = 'https://twitter.com/oauth/authenticate'
callback_url      = 'https://virtualmother-develop.herokuapp.com/user'# テスト環境用
#callback_url      = 'https://virtualmother.herokuapp.com/user'# 本番環境用
#callback_url      = 'https://oauth-test-virtualmother.herokuapp.com/'# T君のテスト用
consumer_key      = os.environ.get("CONSUMER_KEY")  # 各自設定する
consumer_secret   = os.environ.get("CONSUMER_SECRET") # 各自設定する
#################################
# todo 分析できたら別モジュールに移植しましょう
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s') # デバッグ

# 成型
# アクセストークン取得時は {'oauth_token':'トークン', 'oauth_token_secret':'シークレット',…} を返す
# リクエストトークン取得時は {'oauth_token':'トークン',…} を返す
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

# リクエストトークンを取得
def get_request_token():
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    resp, content = client.request('%s?&oauth_callback=%s' % (request_token_url, callback_url))
    url_content = content.decode('utf-8')
    request_token = dict(parse_qsl(url_content))
    return request_token['oauth_token'] # リクエストトークンのみ

# アクセストークンを取得（１）
def get_access_token(oauth_token, oauth_verifier):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(oauth_token, oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url,"POST", body="oauth_verifier={0}".format(oauth_verifier))
    return content

# アクセストークンとアクセストークンシークレットを取得（２）　/authorize 認証済の時に使う
def get_access_token_and_secret(oauth_token, oauth_verifier):
    access_token_and_secret = get_access_token(oauth_token, oauth_verifier).decode('utf-8')
    access_token_and_secret = dict(parse_qsl(access_token_and_secret))
    oauth_token = access_token_and_secret['oauth_token']
    oauth_token_secret = access_token_and_secret['oauth_token_secret']
    return oauth_token,oauth_token_secret
###############################


# トップページ
@app.route('/')
def do_top():
    return render_template('top.html')


# ユーザーページ
@app.route('/user', methods=['POST'])
def check_token():       
    oauth_token = request.args.get('oauth_token', default = "failed", type = str)
    oauth_verifier = request.args.get('oauth_verifier', default = "failed", type = str)
    print(oauth_token,oauth_verifier)

    if oauth_token == "failed" or oauth_verifier == "failed": # 未認証の時
        print("oauth_token or oauth_verifier is failed") # デバッグ
        request_token = get_request_token() # リクエストトークンを取得する
        # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン を作る
        authorize_url = '%s?oauth_token=%s' % (authenticate_url, request_token)
        print(authorize_url) # デバッグ
        # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン に進む
        return redirect(authorize_url)

    else: # 認証済の時
        # アクセストークンとアクセストークンシークレットの取得
        # アクセストークンシークレットの取得
        print("already authorized")
        oauth_token_and_secret = get_access_token_and_secret(oauth_token, oauth_verifier)
        oauth_token        = oauth_token_and_secret[0]
        oauth_token_secret = oauth_token_and_secret[1]
        print("oauth_token:{0} \n oauth_secret:{1}".format(oauth_token,oauth_token_secret))
        api_co    = tweet.ApiConnect(oauth_token,oauth_token_secret)
        user_id   = api_co.see_user_id()
        user_name = api_co.see_user_name()
        
        return render_template('user.html',user_id=user_id,user_name=user_name) # ユーザーページに進む



# ユーザー登録完了ページ
@app.route('/register', methods=['POST'])
def do_register():
    ###（変更）↓ Twitterのスクリーン名を取得して挿入する
    user_id   = request.form['user_id']
    user_name = request.form['user_name']
    ###（変更）↓ TwitterのユーザーIDを取得して挿入する
    do = SendData(user_id)
    db.session.add(do)
    db.session.commit()
    return render_template('register.html',user_name=user_name)
#    request.form[""] # フォームから取得

# 404ページ
#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template(page_not_found.html, 404)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)



