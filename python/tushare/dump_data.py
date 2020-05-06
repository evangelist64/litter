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

os.chdir(os.path.dirname(sys.argv[0]))


df_basic = None
failed_cnts = None
last_cnt = 0
start_time = '2014-01-01'
end_time = '2016-04-16'

def init():
    global df_basic
    global failed_cnt
    global last_cnt
    
    if(os.path.exists('data\\cfg\\stocks_basic.db')):
        df_basic = pd.read_csv('data\\cfg\\stocks_basic.db',dtype=str)
    else:
        df_basic = ts.get_stock_basics()
        df_basic.to_csv('data\\cfg\\stocks_basic.db', encoding='utf-8', index=True)
        
    if(os.path.exists('data\\cfg\\failed_cnts.dt')):
        with open('data\\cfg\\failed_cnts.dt','rb') as f:
            failed_cnts_buffer = f.read()
            failed_cnts = failed_cnts_buffer.split(',')

    if(os.path.exists('data\\cfg\\last_cnt.dt')):
        with open('data\\cfg\\last_cnt.dt','rb') as f:
            last_cnt = int(f.read())
            
def get_remote_data(mysql_con, code):
    try:        
        df_one = ts.get_h_data(code, start=start_time, end=end_time)
        if(df_one is not None):
            #df_one.to_sql('stocks_%s.db'%(idx),mysql_con,flavor='mysql')
            print code
            df_one.to_csv('data\\stocks_%s.db'%(code))
            return True
        else:
            print 'no data,idx:'+code
            return False
    except Exception,e:
        print e
        return False
    
#基础数据存在则直接加载，否则去获取一遍并保存
if __name__ == '__main__':
    
    init()

    conn = MySQLdb.connect(host='127.0.0.1',user='root',db='stocks',passwd='',charset='utf8')
    failed_cnts_file = open('data\\cfg\\failed_cnts.dt','a')
    last_cnt_file = open('data\\cfg\\last_cnts.dt','wb')
    '''
    for i in range(last_cnt,len(df_basic.index)):
        print '-------count:',i
        idx = str(df_basic.code[i])
        if(get_remote_data(conn,idx)):
            last_cnt_file.seek(0)
            last_cnt_file.truncate()
            last_cnt_file.write(str(i))
            last_cnt_file.flush()
        else:
            failed_cnts_file.write(str(i)+',')
            failed_cnts_file.flush()
    '''
    to_load_list = ['002109','300159','603868','603822','603726','603528','603029','300511','300509','300508','300507','002795','000033']
    for i in range(0,len(to_load_list)):
        idx = str(to_load_list[i])
        get_remote_data(conn,idx)

    failed_cnts_file.close()
    last_cnt_file.close()
