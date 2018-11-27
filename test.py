from virtualmother_app.module  import database,tweet
from virtualmother_app import db
from datetime import time

db = database.DBOperation(db)


db.update_get_up_time('1049129656379535360',time(22,10))

do = tweet.MothersTwitter()

#do.call_screen_name("1049129656379535360")

#print(do.call_screen_name("111111"))
