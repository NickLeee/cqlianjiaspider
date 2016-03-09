# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 18:58:22 2016

@author: lenovo
"""
import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb
import time
import datetime


def getonesql(sqlname):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    query = 'select * from '+sqlname+' limit 1;'
    cur.execute(query)
    info = cur.fetchone()
    cur.close()
    conn.close()
    return info
    
def createareaurlSQL():
    currentdate = time.strftime('%Y_%m_%d',time.localtime(time.time())) 
    urlname = 'areaurl_'+currentdate
    urldb = 'url_'+currentdate
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    cur.execute("create table %s like areaurl"%urlname)
    cur.execute("INSERT INTO %s SELECT * FROM areaurl"%urlname)
    conn.commit()
    cur.execute("create table %s like URLdb"%urldb)
    cur.close()
    return urlname,urldb
    
def deleteareaurl(info,areaurlsqlname):
    '''
    info = getonesql returned value
    '''
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    delete = "delete from %s where  url = '%s'"%(areaurlsqlname,info[1])
    cur.execute(delete)
    conn.commit()
    cur.execute("select count(1) from %s;"%areaurlsqlname)
    remainning = cur.fetchone()
    print('url %s delete  remaining %s to get'%(info[1],remainning))
    cur.close()
    conn.close()
    return
    
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
    
def getpageurl(soup,info):
    num = soup.find('div', class_="list-head clear").contents[0].find('span').text
    if int(num)%30 != 0:
        pages = int(num)/30+1
    else:
        pages = int(num)/30
    items = []
    for i in range(pages):
        url = info[1]+'pg'+str(i+1)+'/'
        items.append(url)
    return items
    
def writeSQL(items,sqlname):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    for item in items:
        cur.execute("insert ignore into %s values('%s')"%(sqlname,item))
    conn.commit()
    cur.close()
    return
    
currentdate = time.strftime('%Y_%m_%d',time.localtime(time.time())) 
urlname = 'areaurl_'+currentdate
urldb = 'url_'+currentdate
#newdbname = createareaurlSQL()
newdbname =[urlname,urldb] 
    
while True:
    print'getting one area'
    info = getonesql(newdbname[0])
    soup = getpage(info[1])
    items = getpageurl(soup,info)
    print('writting urlSQL for area %s'%info[2].encode('gbk'))
    writeSQL(items,newdbname[1])
    print'deleting'
    deleteareaurl(info,newdbname[0])

    
