# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 13:41:10 2019

@author: aaaaa
"""

from __future__ import print_function
import time
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import schedule
from pymongo import MongoClient
import urllib.parse
import datetime
import requests
from bs4 import BeautifulSoup

# Authentication Database認證資料庫
Authdb='mystock'

line_bot_api = LineBotApi('VbgVFJ5GcUXalkkCjKXiMVWTrmGW+r3DN9VeZozSLX+Zq4hRXcrS/wI6XPnkLMX5swDxQcjlYuXHdXRBGpdilOJ86xlcmnk8Cuo66GBAS/Wx0DfrzYZFAxbdbo5qmqIS6/Sbz5oa72D8DJ278aRkCQdB04t89/1O/w1cDnyilFU=')
yourid='Ube8f42668a7d9ce94b0728af9b9205eb'
##### 資料庫連接 #####
def constructor():
    client = MongoClient('client = pymongo.MongoClient("mongodb://chuc:chuc0315@@cluster0-shard-00-00-6dvcu.mongodb.net:27017,cluster0-shard-00-01-6dvcu.mongodb.net:27017,cluster0-shard-00-02-6dvcu.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")')
    db = client[Authdb]
    return db

# 抓你的股票
def show_user_stock_fountion():  
    db=constructor()
    collect = db['fountion']
    cel=list(collect.find({"data": 'care_stock'}))
    return cel

def job():
    data = show_user_stock_fountion()
    for i in data:
        stock=i['stock']
        bs=i['bs']
        price=i['price']
        
        url = 'https://tw.stock.yahoo.com/q/q?s=' + stock 
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getstock= soup.find('b').text #裡面所有文字內容
        if float(getstock):
            if bs == '<':
                if float(getstock) < price:
                    get=stock + '的價格：' + getstock
                    line_bot_api.push_message(yourid, TextSendMessage(text=get))
            else:
                if float(getstock) > price:
                    get=stock + '的價格：' + getstock
                    line_bot_api.push_message(yourid, TextSendMessage(text=get))
        else:
            line_bot_api.push_message(yourid, TextSendMessage(text='這個有問題'))
second_5_j = schedule.every(10).seconds.do(job)

# 無窮迴圈
while True: 
    schedule.run_pending()
    time.sleep(1)
