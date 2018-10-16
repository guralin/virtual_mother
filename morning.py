#!/bin/env python
# coding: utf-8

import os
from datetime import datetime

# 「起きて！！！」とTwitterに投稿する
def morning():
    morning_call = "起きて！" + "\n「" + str(datetime.now()) + "」だよ！！！"
    api.PostUpdate(morning_call)

