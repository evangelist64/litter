#coding=utf8
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import os,sys
import matplotlib.pyplot as plt
import numpy as np
import time
import tushare as ts
import MySQLdb
import struct
import datetime

os.chdir(os.path.dirname(sys.argv[0]))

df_basic = None
failed_cnts = None
last_cnt = 0
start_time = '2014-01-01'
end_time = '2016-04-16'
df_all = {}

def init():
    global df_basic
    if(os.path.exists('data\\cfg\\stocks_basic.db')):
        df_basic = pd.read_csv('data\\cfg\\stocks_basic.db',dtype=str)
    else:
        df_basic = ts.get_stock_basics()
        df_basic.to_csv('data\\cfg\\stocks_basic.db', encoding='utf-8', index=True)
              
def get_local_data(code):
    global df_all
    try:        
        df_all[code] = pd.read_csv('data\\stocks_%s.db'%code,dtype={'code':str})
        return True
    except Exception,e:
        print e
        return False

def load_all_data():
    global df_basic
    suc_cnt = 0
    fail_cnt = 0
    for i in range(last_cnt,len(df_basic.index)):
        idx = str(df_basic.code[i])
        if(get_local_data(idx)):
            suc_cnt+=1
            #print 'load %s succeed'%idx

            #for test
            if(suc_cnt>10):
                return
        else:
            fail_cnt+=1
            print '[error] idx:%s'%idx

def show_one_stock_pic(key_one):
    global df_all
    stock_one = df_all[key_one]
    stock_one = stock_one.sort(columns='date')
    stock_one['change'] = stock_one.close - stock_one.open
    #stock_one.plot(figsize=(8,4),kind='line',x='volume',y='change',title=str(key_one))
    stock_one.plot(figsize=(8,4),style='o',x='volume',y='change',title=str(key_one))
    plt.show()
    
    data_cnt = len(stock_one)
    volume_average = sum(stock_one['volume'])/data_cnt
    amount_average = sum(stock_one['amount'])/data_cnt
    print volume_average
    print amount_average

def show_all_stock_pic():
    global df_all
    stock_all = pd.DataFrame()
    for stock_one in df_all.values():
        if(len(stock_all) == 0):
            stock_all = stock_one
        else:
            stock_all = stock_all.append(stock_one)
    stock_all['change'] = stock_all.close - stock_all.open
    stock_all.plot(figsize=(8,4),style='o',x='volume',y='change',title='all stocks')
    plt.show()

def do_calc():
    global df_all
    conti_up_cnt = 0
    total_cnt = 0
    for stock_one in df_all.values():
        stock_one['change'] = stock_one.close - stock_one.open
        cur_day = 0
        cur_day_up = False
        for i in range(0,len(stock_one)):
            last_day = time.mktime(datetime.datetime.strptime(stock_one.iloc[i,0], "%Y-%m-%d").timetuple())
            #有后一天数据
            if(int(cur_day-last_day) == 86400):
                last_day_up = stock_one.iloc[i,7]>0
                if(cur_day_up==True and last_day_up==True):
                    conti_up_cnt+=1
            cur_day = last_day
            cur_day_up = stock_one.iloc[i,7]>0
            if(cur_day_up==True):
                total_cnt+=1
        total_cnt-=1
    print 'conti_up_cnt:',conti_up_cnt
    print 'total_cnt:',total_cnt
    print (float)(conti_up_cnt)/(float)(total_cnt)
    
if __name__ == '__main__':
    init()
    load_all_data()
    #show_one_stock_pic('000014')
    show_all_stock_pic()
    #do_calc()
