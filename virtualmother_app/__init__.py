#!/bin/env python
# coding: utf-8

# appの定義



import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, sqlalchemy

import virtualmother_app.views



app = Flask(__name__)
app.secret_key = '環境変数にSECRET_KEYを設定しておく'

# テスト環境か本番環境のデータベースURLの環境変数を読み込む
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEVELOP_DATABASE_URL') or os.environ.get('MASTER_DATABASE_URL')
# FSADeprecationWarning を消す
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True




