#!/bin/env python
# coding: utf-8

# app, dbの定義

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config.from_object('virtualmother_app.config')

db = SQLAlchemy(app)

import virtualmother_app.views



