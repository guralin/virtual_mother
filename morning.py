#!/bin/env python
# coding: utf-8

import os

from virtualmother_app import db
from virtualmother_app.module import database, tweet
from datetime import datetime,time


do = database.GetData()
users = do.id_and_get_up()

# 今の時刻を10分に取得する
now_time = datetime.now()
now_hour   = now_time.hour
now_minute = now_time.minute
round_down_now_minute = int(now_minute/10)*10

round_down_now_time = time(now_hour,round_down_now_minute)

do = tweet.MothersTwitter()

for user in users:
    db_get_up_time = user[1]
    if db_get_up_time == round_down_now_time:
        print(user[0])
    else:
        print("no")

#print(users)
#print(users[0][1])

# データを取得
#do = database.GetData # GetDataクラスの呼び出し
####（追加） user_idを使って、スクリーン名を取得して、user_nameに格納
#users = db.session.query(do).all() ###（変更）doをuser_nameに変更
#print(f'user_id = {users}')
"""
# tweetする
post = tweet.MothersTwitter()
post.screen_name_call(users)
"""



