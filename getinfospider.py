# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 17:11:30 2016

@author: lenovo
"""

import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb
import time
import random
import datetime
import requests

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
    
def info(soup): 
    allinfo = []
    hlist = soup.find('ul',class_="house-lst")
    bigarea = soup.find('div',class_="option-list").find('a',class_="on").text
    for item in hlist.contents:
        items = ['id_0',
             'url_1',
             'title_2',
             'community_3',
             'rooms_4', 
             'area_5',
             'direction_6',
             'location_7',
             'height_8',
             'year_9',
             'price_10',
             'view_11',
             'ispricereduce_12',
             'isnewsale_13',
             bigarea,
             'unitprice_15']
        items[0] = item.attrs['data-id']
        items[1] = item.contents[0].contents[0].attrs['href']
        info = item.find('div',class_="info-panel")
        items[2] = info.contents[0].text
        items[3] = info.find('div',class_="where").contents[0].text
        items[4] = info.find('div',class_="where").contents[1].text
        mianji = info.find('div',class_="where").contents[2].text.encode('utf-8')
        items[5] = float(re.findall('(.+?)\xe5\xb9\xb3\xe7\xb1\xb3\xc2\xa0\xc2\xa0',mianji)[0])
        if items[5] == 0:
            continue
        items[6] = info.find('div',class_="where").contents[3].text
        items[7] = info.find('div',class_="con").contents[0].text
        items[8] = unicode(info.find('div',class_="con").contents[2])
        if len(info.find('div',class_="con").contents)<4:
            items[9] = 'None'
        else:
            items[9] = unicode(info.find('div',class_="con").contents[4])
        items[10] = float(info.find('div',class_="price").contents[0].text)
        items[11] = int(info.find('div',class_="square").contents[0].contents[0].text)
        pricereduce = info.find('div',class_="price").find('img')
        if pricereduce == None:
            items[12] = 'No'
        else:
            items[12] = 'Yes'
        new = info.find('i',class_="new-label")
        if new == None:
            items[13] = 'No'
        else:
            items[13] = 'Yes'
        items[15] = items[10]/items[5]*10000
        allinfo.append(items)
    return allinfo
    
def writeSQL(info,dbname):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    for item in info:
        cur.execute("insert ignore into "+dbname+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",item)
    conn.commit()
    cur.close()
    return

def getonesql(sqlname):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    query = 'select * from '+sqlname+' limit 1;'
    cur.execute(query)
    info = cur.fetchone()
    cur.close()
    conn.close()
    return info
    
    
def sqlname():
    currentdate = time.strftime('%Y_%m_%d',time.localtime(time.time()))
    urlsqlname = 'url_'+currentdate
    pricesqlname = 'houseprice_'+currentdate
    return urlsqlname,pricesqlname

def deleteurl(info,sqlname):
    '''
    info = getonesql returned value
    '''
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    delete = "delete from %s where  URL = '%s'"%(sqlname,info)
    cur.execute(delete)
    conn.commit()
    print('url %s delete'%(info))

    cur.execute("select count(1) from %s;"%sqlname)
    remainning = cur.fetchone()
    print('remaining %d pages to get'%(remainning[0]))
    cur.close()
    conn.close()
    return



def main():
    name = sqlname()
    while True:
        print('get url')
        starttime = datetime.datetime.now()
        url = getonesql(name[0])[0]
        print('downing page %s'%url)
        soup =getpage(url)
        print('----------')
        items = info(soup)
        print('writeSQL')
        writeSQL(items,name[1])
        deleteurl(url,name[0])
        endtime = datetime.datetime.now()
        timeoffset = str((endtime-starttime).seconds)+'.'+str((endtime - starttime).microseconds)[0:3]
        print('time %s '%timeoffset)
       # time.sleep(2)
main()
