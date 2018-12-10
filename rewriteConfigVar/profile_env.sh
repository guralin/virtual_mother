# !/bin/bash

echo "ローカル環境(~/.profile)のアクセストークンとシークレットを書き換えます"

echo "access_tokenをコピペして貼り付けてください"
read access_token

sed -i  -e "s/export ACCESS_TOKEN=.*$/export ACCESS_TOKEN=\"$access_token\"/g" ~/.profile


echo "access_token_secretをコピペして貼り付けてください"
read access_token_secret
sed -i  -e "s/export ACCESS_TOKEN_SECRET=.*$/export ACCESS_TOKEN_SECRET=\"$access_token_secret\"/g" ~/.profile

source ~/.profile
