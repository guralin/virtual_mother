#!/bin/env python
# coding: utf-8



from datetime import datetime
from random import randint

import twitter, os
api = twitter.Api(consumer_key=os.environ.get("CONSUMER_KEY"),
        consumer_secret=os.environ.get("CONSUMER_SECRET"),
        access_token_key=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"))


# 親クラス
class Twitter():
    def __init__(self):
        self.time = "{0:%H}時{0:%M}分".format(datetime.now())
        self.post_text = "現在の時刻は「{0}」です (^_^)y".format(self.time)

# app.py
class Posts(Twitter):
    def post(self):
        api.PostUpdate(self.post_text)
        return self.post_text

class Replies(Twitter):
    def reply(self, reply_name):
        self.reply_text = "@{0} {1}".format(reply_name, self.post_text)
        api.PostUpdate(self.reply_text)
        return self.reply_text

# morning.py
class MorningCalls(Twitter):
    def call(self, users):
        words = ["起きなさい！",
        "早く起きなさい！",
        "早く起きないと遅刻するよ"]
        for user in users:
            user_name = str(user).split("'")[1]
            word = words[randint(0, (len(words) - 1))]
            morning_call = "@{0}\n もう{1}よ！\n {2}".format(user_name, self.time, word)
            api.PostUpdate(morning_call)



