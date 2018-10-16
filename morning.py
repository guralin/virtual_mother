#!/bin/env python
# coding: utf-8

import os
from datetime import datetime

api = twitter.Api(consumer_key="U84inIJFauv3RUFedHOwzPGLs",
    consumer_secret="VtbtEHaQz2hV3CTachsa29R4JOsLbVkTpxUoTbuSaPmSm5vhOa",
    access_token_key="1049129656379535360-LkXoFhHwr56IEH4TKS0LiE1sTK6VOj",
    access_token_secret="epwTxvBOiqijuDyeuyBdsRk8KyY8JA8PzGpVOD6jLRBIv"
    )

# 「起きて！！！」とTwitterに投稿する
def morning():
    morning_call = "起きて！" + "\n「" + str(datetime.now()) + "」だよ！！！"
    api.PostUpdate(morning_call)

