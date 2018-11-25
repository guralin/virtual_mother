from virtualmother_app.module  import database,tweet
from virtualmother_app import db
from datetime import time

do = database.DBOperation(db)

do.update_get_up_time('1049129656379535360',time(22,30))


do = tweet.MothersTwitter()

print(do.id_for_screen_name("1049129656379535360"))
