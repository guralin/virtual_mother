#!/bin/env python
# coding: utf-8

import os
import codecs
from datetime import datetime
from random import randint
import json
from collections import OrderedDict
import pprint

import twitter # python-twitterライブラリ



class MothersTwitter():

    def __init__(self):
        self.api = twitter.Api(consumer_key    = os.environ.get("CONSUMER_KEY"),
                               consumer_secret = os.environ.get("CONSUMER_SECRET"),
                               access_token_key    = os.environ.get("ACCESS_TOKEN"),
                               access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET"))
        hour = datetime.now().hour
        minute = datetime.now().minute
        self.time = f'{ hour }時{ minute }分'
        try:
            self.status = self.api.VerifyCredentials()
        except twitter.error.TwitterError:
            print("access_token_keyが間違っている可能性があります")


    def call(self, users): # morning.py
        with open('virtualmother_app/module/json/morning_call.json') as morning_call_words:
            words = json.load(morning_call_words)
        for user in users:
            word = words[str(randint(0, (len(words) - 1)))]
            morning_call = f'@{ user }\n もう{ self.time }よ！\n { word }'
            self.api.PostUpdate(morning_call)


# リストを渡す
    def call_screen_names(self, users_id): # morning.py

        with open('virtualmother_app/module/json/morning_call.json') as morning_call_words:
            words = json.load(morning_call_words)

        for user_id in users_id:
            word         = words[str(randint(0, (len(words) - 1)))]
            screen_name  = self.get_screen_name(user_id)
            morning_call = f'@{ screen_name }\n もう{ self.time }よ！\n{ word }'
            self.api.PostUpdate(morning_call)
            print(morning_call)


# 変数を渡す
    def call_screen_name(self, user_id): # morning.py

        with open('virtualmother_app/module/json/morning_call.json') as morning_call_words:
            words = json.load(morning_call_words)

            word  = words[str(randint(0, (len(words) - 1)))]

            try:
                screen_name  = self.get_screen_name(user_id)
                morning_call = f'@{ screen_name }\n もう{ self.time }よ！\n{ word }'
                self.api.PostUpdate(morning_call)
                print(morning_call)

            except twitter.error.TwitterError:
                print("存在しないIDを参照している可能性があります")


    def get_screen_name(self, user_id):
        user = self.api.GetUser(user_id = user_id)
        return user.screen_name


    def dm(self, user_id):
        with open('virtualmother_app/module/json/morning_call.json') as morning_call_words:
            words = json.load(morning_call_words)
            word = words[str(randint(0, (len(words) - 1)))]

            # 環境によってcallback_urlを変える
            if   os.environ.get("environ") == "master":
                 callback_url = 'https://virtualmother.herokuapp.com/wakeup' # 本番環境用

            elif os.environ.get("environ") == "develop":
                 callback_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # テスト環境用

            else:
                 callback_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # ローカル環境用
            morning_call = f'もう{self.time}よ！{word}\n{callback_url}'
            self.api.PostDirectMessage(morning_call, user_id = user_id)


    def response(self, user_id, user_name):
        #word = words[str(randint(0, (len(words) - 1)))]
        greeting = f'{ user_name }\nおはよう (^_^)/\n遅刻しないでね'
        self.api.PostDirectMessage(greeting, user_id)



# テスト用
    def test_tweet(self, tweet_content):
    # このクラスに投稿内容を渡すとその内容でツイートしてくれる
        self.api.PostUpdate(tweet_content)
        print(tweet_content)

    def test_dm(self, tweet_content, friend_id):
        api.PostDirectMessage(tweet_content, screen_name = friend_id)
        print(tweet_content, friend_id)

    def fetch_friend(self):
        users = self.api.GetFriends()
        print([u.name for u in users])

    def return_user(self):
        users = self.api.GetUser(screen_name = "virtual_child")
        print(users.screen_name)
        
    def self_profile(self):
        status = self.api.VerifyCredentials()
        return status



class UsersTwitter():
# api.VerifyCredentials()でインスタンスを作ると、UsersTwitterインスタンスになり、このインスタンスの中にあるid,screen_name,nameなどのキーを指定すると値が返ってくる
    def __init__(self, access_token, access_token_secret):
        self.api = twitter.Api(consumer_key    = os.environ.get("FOR_USER_CONSUMER_KEY"),
                               consumer_secret = os.environ.get("FOR_USER_CONSUMER_SECRET"),
                               access_token_key    = access_token,
                               access_token_secret = access_token_secret)
        try:
            self.status = self.api.VerifyCredentials()
        except twitter.error.TwitterError:
            print("access_token_keyが間違っている可能性があります")


    def see_user_id(self):
        user_id = self.status.id
        return user_id


    def see_screen_name(self):
        screen_name = self.status.screen_name
        return screen_name


    def see_user_name(self):
        user_name = self.status.name
        return user_name



