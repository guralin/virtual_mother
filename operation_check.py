import urllib.request
#with urllib.request.urlopen("http://0.0.0.0:5000/test") as res:
from virtualmother_app.module import tweet
try:
    do = tweet.MothersTwitter()
    tmp=do.self_profile()
    print(f"apiの定期チェック完了")
except:
    print("apiが間違っている可能性があります。Lineにメッセージを送ります")
# 私のLineにメッセージが飛ぶようになっています

    with urllib.request.urlopen("https://guraline.herokuapp.com/test") as res:
       html = res.read().decode("utf-8")
       print(html)
   
