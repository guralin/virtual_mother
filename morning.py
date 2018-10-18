#!/bin/env python
# coding: utf-8

import os
import twitter
from datetime import datetime


api = twitter.Api(consumer_key= os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
    )
# 「起きて！！！」とTwitterに投稿する
morning_call = "起きて！" + "\n「" + str(datetime.now()) + "」だよ！！！"
api.PostUpdate(morning_call)

