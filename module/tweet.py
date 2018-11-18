#!/bin/env python
# coding: utf-8



from datetime import datetime
from random import randint
import json
from collections import OrderedDict
import pprint 
import twitter, os

api = twitter.Api(consumer_key=os.environ.get("CONSUMER_KEY"),
        consumer_secret=os.environ.get("CONSUMER_SECRET"),
        access_token_key=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"))

class Twitter():

    def __init__(self):
        h = datetime.now().hour
        m = datetime.now().minute
        self.time = "{0}時{1}分".format(h, m)

    def call(self, users): # morning.py
        with open('module/json/morning_call.json') as morning_call_words:
           words = json.load(morning_call_words)
        for user in users:
            word = words[str(randint(0, (len(words) - 1)))]
            morning_call = "@{0}\n もう{1}よ！\n {2}".format(user, self.time, word)
            api.PostUpdate(morning_call)

#######################################################
    def test_tweet(self,tweet_content):
#このクラスに投稿内容を渡すとその内容でツイートしてくれる
# （テスト用)
        api.PostUpdate(tweet_content)
        print(tweet_content)

    def test_dm(self,tweet_content,friend_id):
        api.PostDirectMessage(tweet_content,screen_name=friend_id)
        print(tweet_content,friend_id)



