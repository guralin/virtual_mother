from flask import Flask, render_template, g
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
import os
from flask_sqlalchemy import SQLAlchemy # 変更

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )
    app = FlaskWithHamlish(__name__)

    db_uri = "sqlite:///" + os.path.join(app.root_path, 'flasknote.db') # 追加
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri # 追加
    db = SQLAlchemy(app) # 追加

class Entry(db.Model): # 追加
    __tablename__ = "entries" # 追加
    id = db.Column(db.Integer, primary_key=True) # 追加
    title = db.Column(db.String(), nullable=False) # 追加
    body = db.Column(db.String(), nullable=False) # 追加

@app.route('/')
def hello_world():
    entries = Entry.query.all() #変更
    return render_template('index.haml', entries=entries)


# Database
def connect_db():
    db_path = os.path.join(app.root_path, 'flasknote.db')
    rv = sqlite3.connect(db_path)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

