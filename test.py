from virtualmother_app.module  import database,tweet
from virtualmother_app import db
from datetime import time

db = database.DBOperation(db)


db.update_get_up_time('1049129656379535360',time(19,50))
#db.update_get_up_time('1045586841603170305',time(22,50))
#db.update_date('1049129656379535360')
#db.insert_date('1049129656379535360')

#db.db_add('1049129656379535360',time(6,20))

#db.delete_get_up_time('1049129656379535360')

do = tweet.MothersTwitter()
#print(do.return_user())
#do.public_post(1049129656379535360) 

#print(do.self_profile())

#do.test_dm("今日は寒いので体に気をつけてください","33333")
#print(usr.see_user_id())

#do.response('1045586841603170305', 'user_name')

#do.dm(1049129656379535360)

#do.call_screen_name("1049129656379535360")

#print(do.call_screen_name("111111"))
