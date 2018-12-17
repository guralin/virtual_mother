#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request

class OperationCheck():
    def send_line_message(self):
        with urllib.request.urlopen("https://guraline.herokuapp.com/test") as res:
           html = res.read().decode("utf-8")
           print(html)
    
