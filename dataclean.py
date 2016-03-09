# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 15:21:45 2016

@author: lenovo
"""

import pandas as pd
import pandas.io.sql as sql
import MySQLdb
import time

def insert_statice():
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    #cur.excute('INSERT INTO signal_item_statics (date) VALUE (CURDATE());')
    currentdate = time.strftime('%Y_%m_%d',time.localtime(time.time()))
    sqlname = 'houseprice_'+currentdate
    
    cqpd = sql.read_frame('select area,price,view,unitprice from %s'%sqlname,conn)
    
    items= ['avr unit price_0',
            'avr total price_1',
            'total house quantity_2',
            'total house area_3',
            'MID unit price_4',
            'MID total price_5',
            'house quantity viewed_6',
            'AVR viewed times_7'
            ]
    avr = cqpd.mean()
    mid = cqpd.median(axis = 0)
    sumpd = cqpd.sum()
    items[0] = sumpd[1]/sumpd[0]*10000
    items[1] = avr[1]
    items[2] = len(cqpd)
    items[3] = sumpd[0]
    items[4] = mid[3]
    items[5] = mid[1]
    items[6] = len(cqpd[cqpd.view!=0])
    items[7] = cqpd[cqpd.view!=0].sum()[2]/items[6]
    
    cur.execute("insert into signal_item_statics values(CURDATE(),%s,%s,%s,%s,%s,%s,%s,%s)",items)
    conn.commit()
    cur.close()
    return
    
def create_sale_new():
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='cqlianjia_daily_monitoring',charset='utf8')
    cur=conn.cursor()
    currentdate = time.strftime('%Y_%m_%d',time.localtime(time.time()))
    sqlname = 'houseprice_'+currentdate
    predate = time.strftime('%Y_%m_%d',time.localtime(time.time()-24*60*60))
    presqlname = 'houseprice_'+predate
    cur.execute("create table sale_%s as (select * from %s where not ID in (select ID from %s));"%(currentdate,presqlname,sqlname))
    cur.execute("create table new_%s as (select * from %s where not ID in (select ID from %s));"%(currentdate,sqlname,presqlname))
    conn.commit()
    cur.close()
    return
    
create_sale_new()
insert_statice()


    
    
    