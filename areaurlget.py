# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 16:01:40 2016

@author: lenovo
"""


import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb
import time
import random
import datetime


def getpage(url):
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
        content = response.read()
        soup = BeautifulSoup(content)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    return soup
    
url = 'http://cq.lianjia.com/ershoufang/'
soup = getpage(url)
item = soup.find('div', class_="option-list")
referurl = []
for i in item.contents:
    referurl.append(i.attrs['href'])
del referurl[0]
for i in range(11,7,-1):
    del referurl[i]


areaurl = []

for referurli in referurl:
    suburl = 'http://cq.lianjia.com'+referurli
    soupsub = getpage(suburl)
    items = soupsub.find('div', class_="option-list sub-option-list").find_all('a')
    del items[0]
    for i in items:
        a = []
        a.append('http://cq.lianjia.com'+i.attrs['href'])
        a.append(i.text)
        areaurl.append(a)


for area in areaurl:
    area[1] = area[1].encode('utf-8')



def writeSQL(areaurl):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    for item in areaurl:
        cur.execute('insert into areaurl values(%s,%s,%s)',item)
    conn.commit()
    cur.close()
    return
    







