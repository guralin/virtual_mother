from virtualmother_app.module  import database,tweet
from virtualmother_app import db
from datetime import time

db = database.DBOperation(db)


#db.update_get_up_time('1049129656379535360',time(17,30))
#db.update_date('1049129656379535360')
#db.insert_date('1049129656379535360')

#db.db_add('1049129656379535360',time(6,20))

#db.delete_get_up_time('1049129656379535360')

do = tweet.MothersTwitter()

#print(do.self_profile())


#print(usr.see_user_id())

#do.response('1045586841603170305')

#do.dm(1049129656379535360)

#do.call_screen_name("1049129656379535360")

#print(do.call_screen_name("111111"))
