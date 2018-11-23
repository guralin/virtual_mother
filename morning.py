#!/bin/env python
# coding: utf-8

import os

from virtualmother_app import db
from virtualmother_app.module import database, tweet



# データを取得
do = database.GetData # GetDataクラスの呼び出し
###（追加） user_idを使って、スクリーン名を取得して、user_nameに格納
users = db.session.query(do).all() ###（変更）doをuser_nameに変更
print(f'user_id = {users}')
"""
# tweetする
post = tweet.MothersTwitter()
post.screen_name_call(users)
"""



