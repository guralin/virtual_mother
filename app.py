#!/bin/env python
# coding: utf-8

# appの実行

import os

from virtualmother_app import app



if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)



