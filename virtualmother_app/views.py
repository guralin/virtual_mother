#!/bin/env python
# coding: utf-8

import os
from datetime import timedelta, time

from flask import render_template, request, redirect, session
from flask_sqlalchemy import sqlalchemy
import twitter

from virtualmother_app import app, db
from virtualmother_app.module import tweet, token, database, response



# トップページ
@app.route('/')
def do_top():

    # セッションを30分に設定
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes = 30)
    title = "ようこそ"
    #return render_template('top.html', title = title)

    response_content = render_template('top.html', title = title)
    content = response.Response.prepare_response(response_content)
    return content



# ユーザーページ
@app.route('/user', methods = ['GET'])
def check_token():

    try: # セッションがあったら値を代入
        access_token        = str(session['access_token'])
        access_token_secret = str(session['access_token_secret'])

    except: # セッションが無いときはNoneを入れる
        access_token        = 'failed'
        access_token_secret = 'failed'

    if access_token != 'failed' and access_token_secret != 'failed': # セッションがあったとき
        api_co    = tweet.UsersTwitter(access_token, access_token_secret)
        user_name = api_co.see_user_name()
        # ユーザーページに進む
        title = f"{user_name} の部屋"
        #return render_template('user.html', title = title, user_name = user_name)

        response_content = render_template('user.html', title = title, user_name = user_name)
        content = response.Response.prepare_response(response_content)
        return content

    else: # セッションが無いとき
        get_token      = token.Token()
        oauth_token    = request.args.get('oauth_token',    default = 'failed', type = str)
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
            #return redirect(authorize_url)

            response_content = redirect(authorize_url)
            content = response.Response.prepare_response(response_content)
            return content

        else: # セッションに値を登録する
            print("セッションに値を登録する")
            # アクセストークンとアクセストークンシークレットの取得
            # アクセストークンシークレットの取得
            access_token_and_secret = get_token.get_access_token_and_secret(oauth_token, oauth_verifier)
            session['access_token']        = str(access_token_and_secret[0])
            session['access_token_secret'] = str(access_token_and_secret[1])
            #return redirect('/user')

            response_content = redirect('/user')
            content = response.Response.prepare_response(response_content)
            return content



# ユーザー登録完了ページ
@app.route('/register', methods = ['POST'])
def do_register():

    try:
        access_token        = str(session.get('access_token'))
        access_token_secret = str(session.get('access_token_secret'))
        api_co    = tweet.UsersTwitter(access_token, access_token_secret)
        # todo:user_idはdatabase側にstr型で渡さないといけなくなっています
        user_id   = str(api_co.see_user_id())
        user_name = api_co.see_user_name()
        do = database.DBOperation(db)
        
        if request.form['yesno'] == 'yes':
            hour   = int(request.form['hour'])
            minute = int(request.form['minute'])
            get_up_time = time(hour, minute)

            try: # 登録する
                do.insert_get_up_time(user_id, get_up_time)
                title = "登録完了"
                #return render_template('register.html', title = title, user_name = user_name, hour = hour, minute = minute)

                response_content = render_template('register.html', title = title, user_name = user_name, hour = hour, minute = minute)
                content = response.Response.prepare_response(response_content)
                return content

            except sqlalchemy.exc.IntegrityError: # 登録済の時
                #do.update_get_up_time(user_id, get_up_time)←更新したいけど上手くいかなかった
                title = "登録済"
                #return render_template('register.html', title = title, user_name = user_name)

                response_content = render_template('register.html', title = title, user_name = user_name)
                content = response.Response.prepare_response(response_content)
                return content

        elif request.form['yesno'] == 'no': # 解除する

            try:
                do.delete_get_up_time(user_id)
                title = "目覚まし解除"

            except:
                title = "未登録"
                pass

            message = "起こしてほしい時は言ってね"
            #return render_template('register.html', title = title, user_name = user_name, message = message)

            response_content = render_template('register.html', title = title, user_name = user_name, message = message)
            content = response.Response.prepare_response(response_content)
            return content

    except twitter.error.TwitterError: # セッション切れのとき
        #return redirect('/')

        response_content = redirect('/')
        content = response.Response.prepare_response(response_content)
        return content


# 起きたよページ
@app.route("/wakeup")
def wakeup():
    click = tweet.MothersTwitter()
    click.response('1045586841603170305')
    return redirect('/')


# 404ページ
@app.errorhandler(404)
def page_not_found(error):

    title = "ページが見つかりません"
    #return render_template('404-page.html', title = title)

    response_content = render_template('404-page.html', title = title)
    content = response.Response.prepare_response(response_content)
    return content





