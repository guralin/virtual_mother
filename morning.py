#!/bin/env python
# coding: utf-8

import os

from virtualmother_app.module import database, tweet
from datetime import time, timedelta
import datetime



# 今日の日付
today = datetime.date.today()

# 今の時刻を10分ごとに取得する
now_time   = datetime.datetime.now()
now_hour   = now_time.hour
now_minute = now_time.minute
# herokuのスケジューラは10分ごとに動くので1桁目を切り捨ててる
simple_now_minute = int(now_minute / 10) * 10
# 現在の時刻
simple_now_time = time(now_hour, simple_now_minute)
print(f'現在の時刻は、およそ{ simple_now_time }です。')
# 10分前の時刻(replyする時刻)
ten_ago_time   = datetime.datetime.strptime(str(simple_now_time), '%H:%M:%S') + timedelta(minutes = -10)
ten_ago_hour   = int('{:%H}'.format(ten_ago_time))
ten_ago_minute = int('{:%M}'.format(ten_ago_time))
reply_time     = time(ten_ago_hour, ten_ago_minute)
print(reply_time)

mother_tweet = tweet.MothersTwitter()
db = database.GetData()
users_data = db.id_and_get_up()

for user_data in users_data:
    db_user_id     = user_data[0]
    db_get_up_time = user_data[1]
    db_date        = user_data[2]

    if db_get_up_time == simple_now_time:
        print(f'1st send > { db_user_id }に, DMを送ります')
        mother_tweet.morning_dm(db_user_id)

    elif db_get_up_time == reply_time:
        if db_date != today: # まだ起きてない時
            print(f'2nd send > { db_user_id }に, replyを送ります')
            mother_tweet.morning_reply(db_user_id)
        else: # 既に起きている時
            print(f'not send > { db_user_id }は, 起きています')

    else:
        print(f'not send > { db_user_id }の起きる時間は, { db_get_up_time }です')



