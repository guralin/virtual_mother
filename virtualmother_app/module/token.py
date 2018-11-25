#!/bin/env python
# coding: utf-8

import os

import oauth2 as oauth



request_token_url = 'https://twitter.com/oauth/request_token'
access_token_url  = 'https://twitter.com/oauth/access_token'
authenticate_url  = 'https://twitter.com/oauth/authenticate'

# 環境によってcallback_urlを変える
if   os.environ.get("environ") == "master":
    callback_url = 'https://virtualmother.herokuapp.com/user' # 本番環境用

elif os.environ.get("environ") == "develop":
    callback_url = 'https://virtualmother-develop.herokuapp.com/user' # テスト環境用

else:
    callback_url = 'http://127.0.0.1:5000/user' # ローカル環境用
    
consumer_key    = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")



class Token():
    # 成型
    # アクセストークン取得時は {'access_token':'トークン', 'access_token_secret':'シークレット',…} を返す
    # リクエストトークン取得時は {'oauth_token':'トークン',…} を返す
    def parse_qsl(self, url):
        param = {}
        try:
            for i in url.split('&'):
                _p = i.split('=')
                param.update({_p[0]: _p[1]})
        except:
            param['oauth_token']        = 'failed'
            param['oauth_token_secret'] = 'failed'
        return param
    
    # リクエストトークンを取得
    def get_request_token(self):
        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        client   = oauth.Client(consumer)
        resp, content = client.request('%s?&oauth_callback=%s' % (request_token_url, callback_url))
        url_content   = content.decode('utf-8')
        request_token = dict(self.parse_qsl(url_content))
        return request_token['oauth_token'] # リクエストトークンのみ

    # アクセストークンを取得（１）
    def get_access_token(self, oauth_token, oauth_verifier):
        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        token    = oauth.Token(oauth_token, oauth_verifier)
        client   = oauth.Client(consumer, token)
        resp, content = client.request(access_token_url, "POST", body="oauth_verifier={0}".format(oauth_verifier))
        return content

    # アクセストークンとアクセストークンシークレットを取得（２）　/authorize 認証済の時に使う
    def get_access_token_and_secret(self, oauth_token, oauth_verifier):
        access_token_and_secret = self.get_access_token(oauth_token, oauth_verifier).decode('utf-8')
        dict_access_token_and_secret = dict(self.parse_qsl(access_token_and_secret))
        access_token        = dict_access_token_and_secret['oauth_token']
        access_token_secret = dict_access_token_and_secret['oauth_token_secret']
        return access_token, access_token_secret




