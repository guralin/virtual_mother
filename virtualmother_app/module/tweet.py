#!/bin/env python
# coding: utf-8

import os
import codecs
from datetime import datetime
from random import randint
import json
from collections import OrderedDict
import pprint
from virtualmother_app.module import database,token_check
import twitter # python-twitterライブラリ



class MothersTwitter():

    def __init__(self):

        self.api = twitter.Api(consumer_key    = os.environ.get('CONSUMER_KEY'),
                               consumer_secret = os.environ.get('CONSUMER_SECRET'),
                               access_token_key    = os.environ.get('ACCESS_TOKEN'),
                               access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET'))

        hour   = datetime.now().hour
        minute = datetime.now().minute
        self.time = f'{ hour }時{ minute }分'

        try:
            self.status = self.api.VerifyCredentials()

        except twitter.error.TwitterError:
            print('access_token_keyが間違っている可能性があります')
            oc = token_check.OperationCheck()
            oc.send_line_message()

            


    def morning_dm(self, user_id): # morning.py

        with open('virtualmother_app/module/json/morning_call.json') as morning_call_words:
            words = json.load(morning_call_words)
            word = words[str(randint(0, (len(words) - 1)))]

            # 環境によってリンクを変える
            if   os.environ.get('environ') == 'master':
                 link_url = 'https://virtualmother.herokuapp.com/wakeup' # 本番環境用

            elif os.environ.get('environ') == 'develop':
                 link_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # テスト環境用

            else:
                 link_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # ローカル環境用

            morning_call = f'もう{self.time}よ！\n{word}\n{link_url}'
            print(f'===<Message>===\n{morning_call}\n===============')

            try:
                self.api.PostDirectMessage(morning_call, user_id)

            except KeyError:
                print("存在しないIDを参照している可能性があります\nヒント：デバック用に変なIDを入れてないですか？")



    def response(self, user_id, user_name): # /wakeup (DMのリンクがクリックされた時)
        todo_db = database.TodoData()
        todos= todo_db.get_todolist_from_single_user(user_id)

        """ 
            表示されるtodo_wordsの例
            <user_name>おはよう！
            しっかり起きられて偉いわ！
            教えてもらったことを確認するわね
            <todo>
            <todo>
            ...
            大丈夫？忘れていることはない？
        """
        todo_words= ""

            #listのtodosの中身が空である場合はfalseを返すみたいです
        if todos:
            for todo in todos:
                todo ="「" + todo + "」"
                todo_words += todo
            todo_words +="って言っていたけど大丈夫？忘れていることはない？"
        else:
            todo_words +="・・・\n朝忘れそうなことがあったらお母さんに教えてね\n"
            todo_words +="明日から伝えるわ\n"
            todo_words +="つ https://virtualmother.herokuapp.com/todoapp"


        greeting = f'{ user_name }\nおはよう (^_^)/\nしっかり起きられて偉いわ！\n {todo_words}'
        self.api.PostDirectMessage(greeting, user_id)


    def get_screen_name(self, user_id):

        user = self.api.GetUser(user_id)
        return user.screen_name


    def morning_reply(self, user_id): # morning.py (10分以内に起きなかった時)

        with open('virtualmother_app/module/json/morning_call.json') as morning_call_words:
            words = json.load(morning_call_words)
            word = words[str(randint(0, (len(words) - 1)))]

        # 環境によってリンクを変える
        if   os.environ.get('environ') == 'master':
            link_url = 'https://virtualmother.herokuapp.com/wakeup' # 本番環境用

        elif os.environ.get('environ') == 'develop':
            link_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # テスト環境用

        else:
            link_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # ローカル環境用

        try:
            user_name = self.get_screen_name(user_id)
            morning_call = f'@{user_name}\nもう{self.time}よ！ 10分過ぎてるよ！\n{word}\n{link_url}'
            print(f'===<Message>===\n{morning_call}\n===============')
            self.api.PostUpdate(morning_call)

        except KeyError:
            print("存在しないIDを参照している可能性があります\nヒント：デバック用に変なIDを入れてないですか？")



    def get_user_name(self, user_id):

        user = self.api.GetUser(user_id)
        return user.name



    def public_post(self,user_id):

        with open('virtualmother_app/module/json/public_call.json') as morning_call_words:
            words = json.load(morning_call_words)
            word = words[str(randint(0, (len(words) - 1)))]

        # 環境によってリンクを変える
        if   os.environ.get('environ') == 'master':
            link_url = 'https://virtualmother.herokuapp.com/wakeup' # 本番環境用

        elif os.environ.get('environ') == 'develop':
            link_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # テスト環境用

        else:
            link_url = 'https://virtualmother-develop.herokuapp.com/wakeup' # ローカル環境用

        try:
            user_name = self.get_user_name(user_id)
            screen_name = self.get_screen_name(user_id)
            morning_call = f'もう{self.time}よ！ 20分過ぎてるよ！\n{user_name}(@{screen_name}){word}'
            print(f'===<Message>===\n{morning_call}\n===============')
            self.api.PostUpdate(morning_call)

        except KeyError:
            print("存在しないIDを参照している可能性があります\nヒント：デバック用に変なIDを入れてないですか？")





# テスト用
    def test_tweet(self, tweet_content):
    # このクラスに投稿内容を渡すとその内容でツイートしてくれる
        self.api.PostUpdate(tweet_content)
        print(tweet_content)

    def test_dm(self, tweet_content, user_id):
        self.api.PostDirectMessage(tweet_content, user_id = user_id)
        print(tweet_content, user_id)

    def fetch_friend(self):
        users = self.api.GetFriends()
        print([u.name for u in users])

    def return_user(self):
        users = self.api.GetUser(screen_name = "virtual_child")
        print(users.name)
        
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



