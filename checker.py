# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from requests import exceptions
import uuid
import sys
import os
import re

target_dir = "./test/"

target_url = sys.argv[1]
responce = ''
try:
  response = requests.get(str(target_url))
except exceptions.SSLError as e:
  print ("SSLError: " + target_url)

## 中身チェック
soup = BeautifulSoup(response.text, 'html.parser')
## 結果を格納するディレクトリ
target = soup.title.string[0:5].strip()
## 取得したコンテンツからimgタグを抽出
imgs = soup.select('img')

for img in imgs:
  ## imgタグのリンクをhttpsに変更
  link = re.sub("^http:", "https:", img['src'] ,1)
  ## 検証
  try:
    requests.get(link)
  except exceptions.SSLError as e :
      with open(str(target_dir) + '/link_error' + str('.txt'), 'w') as file:
        file.write(str(img['src']))
      continue