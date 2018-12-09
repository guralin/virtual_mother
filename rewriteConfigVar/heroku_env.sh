# !/bin/bash

# access_tokenとsecretをコピペして貼り付けるだけで
# ローカル環境、テスト環境、本番環境すべてが書き換わります
# readはpythonでいうinput()。 引数に指定した変数に入力した値が格納される

echo "caution! : herokuの環境変数が書き換わります。間違った値を入力するとHerokuが動かなくなります"

echo "ACCESS_TOKENをコピペしてエンターキーを押してください"
read access_token

echo "本当に書き換えてしまって大丈夫ですか？だめならCtrl+Cで終了させてください"
read t

heroku config:set ACCESS_TOKEN="$access_token" --app virtualmother-develop
heroku config:set ACCESS_TOKEN="$access_token" --app virtualmother


echo "ACCESS_TOKEN_SECRETをコピペしてエンターキーを押してください"
read access_token_secret

echo "本当に書き換えてしまって大丈夫ですか？だめならCtrl+Cで終了させてください"
read t

heroku config:set ACCESS_TOKEN="$access_token" --app virtualmother-develop
heroku config:set ACCESS_TOKEN="$access_token" --app virtualmother


