#!/bin/env python
# coding: utf-8

# appの定義



import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, sqlalchemy



app = Flask(__name__)

app.config.from_object('virtualmother_app.config')

db = SQLAlchemy(app)

import virtualmother_app.views



