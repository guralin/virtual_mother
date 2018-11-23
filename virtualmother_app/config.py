#!/bin/env python
# coding: utf-8

# appの設定



import os

from virtualmother_app import app



app.secret_key = '環境変数にSECRET_KEYを設定しておく'

# テスト環境か本番環境のデータベースURLの環境変数を読み込む
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')

# FSADeprecationWarning を消す
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



