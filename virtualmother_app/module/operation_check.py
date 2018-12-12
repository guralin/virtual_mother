import urllib.request
#with urllib.request.urlopen("http://0.0.0.0:5000/test") as res:
import tweet
try:
    do = tweet.MothersTwitter()
    do.self_profile()
except:
    print("apiが間違っている可能性があります。Lineにメッセージを送ります")

    with urllib.request.urlopen("https://guraline.herokuapp.com/test") as res:
       html = res.read().decode("utf-8")
       print(html)
   
