#!/bin/env python
# coding: utf-8

from datetime import datetime
hour = datetime.now().hour
minute = datetime.now().minute
second = datetime.now().second
time = "{0}時{1}分{2}秒".format(hour, minute,second)

import twitter, os
api = twitter.Api(consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token_key=os.environ.get("ACCESS_TOKEN"),
    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET")
    )

class Posts():
    def __init__(self):
        self.post_text = "現在の時刻は「{0}」です (^_^)y".format(time)
    def twitter_upload(self):
        api.PostUpdate(self.post_text)
        return self.post_text

