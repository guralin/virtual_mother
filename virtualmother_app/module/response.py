#!/bin/env python
# coding: utf-8

from flask import make_response



class Response():

    def prepare_response(response_content):
        response = make_response(response_content)
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains' # httpsを強制
        response.headers['Content-Security-Policy'] = "default-src 'self' twitter.com use.fontawesome.com" # 読み込みを許可するドメインを指定
        response.headers['X-Content-Type-Options'] = 'nosniff' # 指定したコンテントタイプを強制
        response.headers['X-Frame-Options'] = 'SAMEORIGIN' # htmlのframeやiframeで呼び出すのを許可するドメインを指定
        response.headers['X-XSS-Protection'] = '1; mode=block' # ブラウザのセキュリティを利用
        return response
