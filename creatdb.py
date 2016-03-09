# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 20:32:50 2016

@author: lenovo
"""


import MySQLdb
import time



def createareaurlSQL():
    currentdate = time.strftime('%Y_%m_%d',time.localtime(time.time())) 
    urlname = 'areaurl_'+currentdate
    urldb = 'url_'+currentdate
    sqlname = 'houseprice_'+currentdate
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    cur.execute("create table %s like areaurl"%urlname)
    cur.execute("INSERT INTO %s SELECT * FROM areaurl"%urlname)
    conn.commit()
    cur.execute("create table %s like URLdb"%urldb)
    conn.commit()
    cur.execute("create table %s like housepricedb"%sqlname)
    conn.commit()
    cur.close()
    return 
    
createareaurlSQL()