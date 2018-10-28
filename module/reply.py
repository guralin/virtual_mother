#!/bin/env python
# coding: utf-8

from datetime import datetime

import twitter, os
api = twitter.Api(consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token_key=os.environ.get("ACCESS_TOKEN"),
    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET")
    )

class Reply():
    def __init__(self):
        hour = datetime.now().hour
        minute = datetime.now().minute
        time = "{0}時{1}分".format(hour, minute)
        self.post_text = "現在の時刻は「{0}」です (^_^)y".format(time)
    def send_reply(self, reply_name):
        self.reply_post = "@{0} {1}".format(reply_name, self.post_text)
        api.PostUpdate(self.reply_post)
        return self.reply_post

