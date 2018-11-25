#!/bin/env python
# coding: utf-8

import os
from datetime import timedelta

from flask import render_template, request, redirect, session
from flask_sqlalchemy import sqlalchemy
import twitter

from virtualmother_app import app, db
from virtualmother_app.module import tweet, token, database



# トップページ
@app.route('/')
def do_top():
    # セッションを30分に設定
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes = 30)
    title = "ようこそ"
    return render_template('top.html', title = title)



# ユーザーページ
@app.route('/user', methods = ['GET', 'POST'])
def check_token():
    try: # セッションがあったら値を代入
        access_token        = session['access_token']
        access_token_secret = session['access_token_secret']

    except: # セッションが無いときはNoneを入れる
        access_token        = 'failed'
        access_token_secret = 'failed'

    if access_token != 'failed' and access_token_secret != 'failed': # セッションがあったとき
        api_co    = tweet.UsersTwitter(access_token, access_token_secret)
        user_name = api_co.see_user_name()
        # ユーザーページに進む
        title = f"{user_name} の部屋"
        return render_template('user.html', title = title, user_name = user_name)

    else: # セッションが無いとき
        get_token      = token.Token()
        oauth_token    = request.args.get('oauth_token', default = 'failed', type = str)
        oauth_verifier = request.args.get('oauth_verifier', default = 'failed', type = str)
        print(f'oauth_token = {oauth_token}, oauth_verifier = {oauth_verifier}')

        if oauth_token == 'failed' or oauth_verifier == 'failed': # Oauth認証する
            print("Oauth認証する")
            request_token = get_token.get_request_token() # リクエストトークンを取得する
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン を作る
            authenticate_url = 'https://twitter.com/oauth/authenticate'
            authorize_url    = '%s?oauth_token=%s' % (authenticate_url, request_token) 
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン に進む
            print(f'認証ページに進む ({authorize_url})')
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
        access_token        = session.get('access_token')
        access_token_secret = session.get('access_token_secret')
        api_co    = tweet.UsersTwitter(access_token, access_token_secret)
        user_id   = api_co.see_user_id()
        user_name = api_co.see_user_name()

        try: # 登録する
            do = database.DBOperation(db)
            #フォームから取得した時刻をtimeモジュールget_up_timeに渡してください
            #起床時間が変数として設定されていない場合は自動的に7時として設定します
            try:
                do.db_add(user_id, get_up_time)

            except NameError: # get_up_timeが定義されていないとき
                do.db_add(user_id)

            title = "登録完了"
            return render_template('register.html', title = title, user_name = user_name, user_id = user_id)

        except sqlalchemy.exc.IntegrityError: # 登録済み
            title = "登録済"
            return render_template('register.html', title = title, user_name = user_name)

    except twitter.error.TwitterError: # セッション切れのとき
        return redirect('/')



# 404ページ
@app.errorhandler(404)
def page_not_found(error):
    title = "ページが見つかりません"
    return render_template('404-page.html', title = title)





