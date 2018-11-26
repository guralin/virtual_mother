#!/bin/env python
# coding: utf-8

import os

from virtualmother_app import db
from virtualmother_app.module import database, tweet
from datetime import datetime,time


db = database.GetData()
users = db.id_and_get_up()

# 今の時刻を10分に取得する
now_time = datetime.now()
now_hour   = now_time.hour
now_minute = now_time.minute
# herokuのスケジューラがたまに１分遅れるので切り捨ててる
round_down_now_minute = int(now_minute / 10) * 10

round_down_now_time = time(now_hour, round_down_now_minute)
print(f"現在の時刻は{round_down_now_time}です")

mother_tweet = tweet.MothersTwitter()

for user in users:
    db_user_id     = user[0]
    db_get_up_time = user[1]
    if db_get_up_time == round_down_now_time:
        mother_tweet.call_screen_name(db_user_id)
    else:
        print(f"not match > user_id:{db_user_id} の起きる時間は{db_get_up_time}です")



