#!/bin/env python
# coding: utf-8

import os
from datetime import timedelta, time

from flask import render_template, request, redirect, session
from flask_sqlalchemy import sqlalchemy
import twitter
from time import sleep

from virtualmother_app import app, db
from virtualmother_app.module import tweet, token, database, response



# トップページ
@app.route('/')
def do_top():
# /logoutにてセッションの有効期限を0秒にしたのを30分に直しています

    print(f"/ セッションの有効期限:{app.permanent_session_lifetime}")
    title = "おかえりなさい"
    #return render_template('top.html', title = title)
    response_content = render_template('top.html', title = title)
    content = response.Response.prepare_response(response_content)
    return content



# ユーザーページ
@app.route('/user', methods = ['GET'])
def check_token():

    try: # セッションがあったら値を代入
        print(f"/user (is_session)セッションの有効期限:{app.permanent_session_lifetime}")
        access_token        = str(session['access_token'])
        access_token_secret = str(session['access_token_secret'])

    except: # セッションが無いときは'failed'を入れる
        access_token        = 'failed'
        access_token_secret = 'failed'

    if access_token != 'failed' and access_token_secret != 'failed': # セッションがあったとき
        api_co    = tweet.UsersTwitter(access_token, access_token_secret)
        user_name = api_co.see_user_name()
        user_id   = str(api_co.see_user_id())
        
        try:
            get_db      = database.GetData()
            get_up_time = get_db.get_up_time(user_id)
            get_up_text =f"{get_up_time.hour}時{get_up_time.minute}分"
        except AttributeError:
            get_up_text ="未設定" 

        

        



        # ユーザーページに進む
        title = f"{user_name} の部屋"
        #return render_template('user.html', title = title, user_name = user_name)
        response_content = render_template('user.html', title = title, user_name = user_name, get_up_text= get_up_text)
        content = response.Response.prepare_response(response_content)
        return content

    else: # セッションが無いとき
        get_token      = token.Token()
        oauth_token    = request.args.get('oauth_token',    default = 'failed', type = str)
        oauth_verifier = request.args.get('oauth_verifier', default = 'failed', type = str)
        print(f'oauth_token = {oauth_token}\noauth_verifier = {oauth_verifier}')

        if oauth_token == 'failed' or oauth_verifier == 'failed': # Oauth認証する
            print("Oauth認証する")
            request_token = get_token.get_request_token() # リクエストトークンを取得する
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン を作る
            authenticate_url = 'https://twitter.com/oauth/authenticate'
            authorize_url    = '%s?oauth_token=%s' % (authenticate_url, request_token) 
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン に進む

            print(f'認証ページに進む ({authorize_url})')
            #return redirect(authorize_url)
            response_content = redirect(authorize_url)
            content = response.Response.prepare_response(response_content)
            return content

        else: # セッションに値を登録する
            print("セッションに値を登録する")
            # アクセストークンとアクセストークンシークレットの取得
            # アクセストークンシークレットの取得
            access_token_and_secret = get_token.get_access_token_and_secret(oauth_token, oauth_verifier)
            # /logoutにてセッションの有効期限を0秒にしたのを30分に直しています
            print(f"/user (session入力前)セッションの有効期限:{app.permanent_session_lifetime}")
            app.permanent_session_lifetime = timedelta(minutes = 30)
            session['access_token']        = str(access_token_and_secret[0])
            session['access_token_secret'] = str(access_token_and_secret[1])
            print(f"/user (session入力後)セッションの有効期限:{app.permanent_session_lifetime}")

            #return redirect('/user')
            response_content = redirect('/user')
            content = response.Response.prepare_response(response_content)
            return content



# ユーザー登録完了ページ
@app.route('/register', methods = ['POST'])
def do_register():

    try:
        print(f"/register セッションの有効期限:{app.permanent_session_lifetime}")
        access_token        = str(session.get('access_token'))
        access_token_secret = str(session.get('access_token_secret'))
# うまくセッションが渡せてないと"access_token_keyが間違っている可能性があります"と出る
        api_co    = tweet.UsersTwitter(access_token, access_token_secret)
        # todo:user_idはdatabase側にstr型で渡さないといけなくなっています
        user_id   = str(api_co.see_user_id())
        user_name = api_co.see_user_name()
        do = database.DBOperation(db)
        
        if request.form['yesno'] == 'yes':
            hour   = int(request.form['hour'])
            minute = int(request.form['minute'])
            get_up_time = time(hour, minute)

            try: # 登録情報の更新
                do.update_get_up_time(user_id, get_up_time)
                title = "登録完了"

            except AttributeError: # 新規登録
                do.insert_get_up_time(user_id, get_up_time)
                title = "新規登録完了"

            #return render_template('register.html', title = title, user_name = user_name, hour = hour, minute = minute)
            response_content = render_template('register.html', title = title, user_name = user_name, hour = hour, minute = minute)
            content = response.Response.prepare_response(response_content)
            return content

        elif request.form['yesno'] == 'no': # 起こしてほしくない時

            try:
                do.delete_get_up_time(user_id)
                title = "目覚まし解除"

            except AttributeError:
                title = "未登録"

            #return render_template('register.html', title = title, user_name = user_name)
            response_content = render_template('register.html', title = title, user_name = user_name)
            content = response.Response.prepare_response(response_content)
            return content

    except twitter.error.TwitterError: # セッション切れのとき
        #return redirect('/')
        response_content = redirect('/')
        content = response.Response.prepare_response(response_content)
        return content

    except AttributeError: # セッションを上手く読めなかったとき
        #return redirect('/user')
        response_content = redirect('/user')
        content = response.Response.prepare_response(response_content)
        return content



# DMのリンクがクリックされたら処理をして、Twitterのホームにリダイレクトする
@app.route("/wakeup")
def wakeup():

    try: # セッションがあったら値を代入
        access_token        = str(session['user_access_token'])
        access_token_secret = str(session['user_access_token_secret'])

    except: # セッションが無いときは'failed'を入れる
        access_token        = 'failed'
        access_token_secret = 'failed'

    if access_token != 'failed' and access_token_secret != 'failed': # セッションがあったとき
        print(f'access_token = {access_token}\naccess_token_secret = {access_token_secret}')
        # DMで返信する
        api_co    = tweet.UsersTwitter(access_token, access_token_secret)
        user_id   = str(api_co.see_user_id())
        user_name = str(api_co.see_user_name())
        print(f'user_id = {user_id}\nuser_name = {user_name}')
        click = tweet.MothersTwitter()
        click.response(user_id, user_name)
        # データベースの日付を更新
        do = database.DBOperation(db)
        do.update_date(user_id)

        # Twitterのホームに戻る
        #return redirect('https://twitter.com')
        response_content = redirect('https://twitter.com')
        content = response.Response.prepare_response(response_content)
        return content

    else: # セッションが無いとき
        get_token      = token.Token()
        oauth_token    = request.args.get('oauth_token',    default = 'failed', type = str)
        oauth_verifier = request.args.get('oauth_verifier', default = 'failed', type = str)
        print(f'oauth_token = {oauth_token}, oauth_verifier = {oauth_verifier}')

        if oauth_token == 'failed' or oauth_verifier == 'failed': # Oauth認証する
            print("Oauth認証する")
            request_token = get_token.get_request_token_wakeup() # リクエストトークンを取得する
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン を作る
            authenticate_url = 'https://twitter.com/oauth/authenticate'
            authorize_url    = '%s?oauth_token=%s' % (authenticate_url, request_token) 
            # https://twitter.com/oauth/authenticate?oauth_token=リクエストトークン に進む

            print(f'認証ページに進む ({authorize_url})')
            #return redirect(authorize_url)
            response_content = redirect(authorize_url)
            content = response.Response.prepare_response(response_content)
            return content

        else: # セッションに値を登録する
            print("セッションに値を登録する")
            # アクセストークンとアクセストークンシークレットの取得
            # アクセストークンシークレットの取得
            access_token_and_secret = get_token.get_access_token_and_secret(oauth_token, oauth_verifier)
            # /logoutにてセッションの有効期限を0秒にしたのを30分に直しています
            app.permanent_session_lifetime = timedelta(minutes = 30)
            session['user_access_token']        = str(access_token_and_secret[0])
            session['user_access_token_secret'] = str(access_token_and_secret[1])


            #return redirect('/wakeup')
            response_content = redirect('/wakeup')
            content = response.Response.prepare_response(response_content)
            return content



# ログアウト
@app.route("/logout")
def logout():

    # セッションを0秒に設定
    print(f"/logout セッションの有効期限:{app.permanent_session_lifetime}")
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds = 0)
    #sleep(2)

    print(f"/logout (0秒適応)セッションの有効期限:{app.permanent_session_lifetime}")
    session.pop('access_token', None)
    session.pop('access_token_secret', None)

    #return redirect('/')
    response_content = redirect('/')
    content = response.Response.prepare_response(response_content)
    return content





# 404ページ
@app.errorhandler(404)
def page_not_found(error):

    title = "ページが見つかりません"
    #return render_template('404-page.html', title = title)
    response_content = render_template('404-page.html', title = title)
    content = response.Response.prepare_response(response_content)
    return content


