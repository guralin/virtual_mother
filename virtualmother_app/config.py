#!/bin/env python
# coding: utf-8

# appの設定

import os

from virtualmother_app import app


#secret_key_text = 
app.secret_key = f"{os.environ.get('SECRET_KEY')}"

# テスト環境か本番環境のデータベースURLの環境変数を読み込む
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')

# FSADeprecationWarning を消す
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Cookieの設定
#app.config.update(SESSION_COOKIE_SECURE = True, SESSION_COOKIE_SAMESITE = 'Lax', SESSION_COOKIE_HTTPONLY = True)



