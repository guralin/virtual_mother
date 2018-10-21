#!/bin/env python
# coding: utf-8

from datetime import datetime
hour = datetime.now().hour
minute = datetime.now().minute
time = "{0}時{1}分".format(hour, minute)

import twitter, os
api = twitter.Api(consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token_key=os.environ.get("ACCESS_TOKEN"),
    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET")
    )

class Post():
    def __init__(self):
        post_text = "現在の時刻は「{0}」です (^_^)y".format(time)
        api.PostUpdate(post_text)
    def post_text(self):
        post_text = "現在の時刻は「{0}」です (^_^)y".format(time)
        return post_text

