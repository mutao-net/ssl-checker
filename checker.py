# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from requests import exceptions
import uuid
import sys
import os
import re

def check(imgs):
  target_dir = "./test/"
  for img in imgs:
    ## imgタグのリンクをhttpsに変更
    if 'src' in img.attrs:
      link = re.sub("^http:", "https:", img['src'] ,1)
    else :
      print("src not exists")
      continue
    print("check!: " + link)
    ## 検証
    try:
     requests.get(link)
    except exceptions.SSLError :
        with open(str(target_dir) + '/link_error' + str('.txt'), mode='a') as file:
          file.write(str(img['src']) + "\n")
        continue
    except Exception :
      continue

def main():
  target_url = sys.argv[1]
  response = ''
  try:
    response = requests.get(str(target_url))
  except exceptions.SSLError:
    print ("SSLError: " + target_url)

  ## 中身チェック
  soup = BeautifulSoup(response.text, 'html.parser')
  imgs = soup.select('img')
  check(imgs)
  ## 結果を格納するディレクトリ
  #target = soup.title.string[0:5].strip()

  atags = soup.select('a')
  for atag in atags:
    href = atag['href']
    if (re.match(r"(http:|https)", href) == None):
      print("continue" + href)
      continue
    response = requests.get(href)
    soup = BeautifulSoup(response.text, 'html.parser')
    ## 取得したコンテンツからimgタグを抽出
    imgs = soup.select('img')
    check(imgs)
if __name__ == "__main__":
  main()
