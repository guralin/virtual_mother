#!/bin/env python
# coding: utf-8

import os

from module import tweet, token

from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta

app = Flask(__name__)
app.secret_key = '環境変数にSECRET_KEYを設定しておく'
app.debug = True

#####データベース関連###############
# テスト環境か本番環境のデータベースURLの環境変数を読み込む
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')
# FSADeprecationWarning を消す
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



# トップページ
@app.route('/')
def do_top():
    # セッションを30分に設定
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    return render_template('top.html')


# ユーザーページ
@app.route('/user', methods=['GET', 'POST'])
def check_token():
    get_token = token.Token()
    try: # セッションがあったら値を代入
        access_token = session['access_token']
        access_token_secret = session['access_token_secret']
    except: # セッションが無いときはNoneを入れる
        access_token = None
        access_token_secret = None

    if access_token != None and access_token_secret != None: # セッションがあったとき
        api_co    = tweet.ApiConnect(access_token, access_token_secret)
        user_name = api_co.see_user_name()
        # ユーザーページに進む
        return render_template('user.html', user_name=user_name)
    else: # セッションが無いとき
        oauth_token = request.args.get('oauth_token', default = None, type = str)
        oauth_verifier = request.args.get('oauth_verifier', default = None, type = str)
        print(f'oauth_token={oauth_token}, oauth_verifier={oauth_verifier}')
        if oauth_token == None or oauth_verifier == None: # Oauth認証する
            print("Oauth認証する")
            request_token = get_token.get_request_token() # リクエストトークンを取得する
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン を作る
            authenticate_url = 'https://twitter.com/oauth/authenticate'
            authorize_url = '%s?oauth_token=%s' % (authenticate_url, request_token)
            print(authorize_url) # デバッグ
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン に進む
            return redirect(authorize_url)

        else: # セッションに値を登録する
            print("セッションに値を登録する")
            # アクセストークンとアクセストークンシークレットの取得
            # アクセストークンシークレットの取得
            access_token_and_secret = get_token.get_access_token_and_secret(oauth_token, oauth_verifier)
            session['access_token']        = access_token_and_secret[0]
            session['access_token_secret'] = access_token_and_secret[1]
            return redirect('/user')


# ユーザー登録完了ページ
@app.route('/register')
def do_register():
    try:
        access_token = session.get('access_token')
        access_token_secret = session.get('access_token_secret')
        api_co    = tweet.ApiConnect(access_token, access_token_secret)
        user_id   = api_co.see_user_id()
        user_name = api_co.see_user_name()
        try: # 登録する
            do = SendData(user_id)
            db.session.add(do)
            db.session.commit()
            return render_template('register.html', user_name=user_name, user_id=user_id)
        except: # 登録済み
            return render_template('register.html', user_name=user_name)
    except: # セッション切れのとき
        return redirect('/')



# 404ページ
#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template(page_not_found.html, 404)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)



