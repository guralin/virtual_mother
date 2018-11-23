#!/bin/env python
# coding: utf-8

import os

from virtualmother_app import app

port = int(os.environ.get('PORT', 5000))
app.run(port=port)
