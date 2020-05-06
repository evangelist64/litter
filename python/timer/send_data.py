#coding=gbk
import time,sched,os
import urllib
import httplib
import json
import MySQLdb
import os,sys
import time
import datetime

cur_dir = os.path.dirname(sys.argv[0])
os.chdir(cur_dir)

appKey = "206"
groupId = "205"

s = sched.scheduler(time.time,time.sleep)
cfg_global = {}

def sched_func(inc):
    s.enter(inc,0,sched_func,(inc,))
    do_send_data()

def do_send_data():
    cur_time = time.time()
    now_tm = time.localtime(cur_time)
    last_day_tm = time.localtime(cur_time-86400)
    #-----------从数据库查log数据(昨天的所有数据)
    login_table_name = "tbl_login_%s"%(time.strftime('%Y%m%d',last_day_tm))
    print "-------------send data,%s-------------"%datetime.datetime.fromtimestamp(cur_time)
    sql_login = "SELECT * from %s where op_type=1006 or op_type=1002 or op_type=1005"%(login_table_name)
    conn = MySQLdb.connect(host=cfg_global['db_host'],user=cfg_global['db_user'],db=cfg_global['db_name_log'],passwd=cfg_global['db_passwd'],charset=cfg_global['db_charset'])
    cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    cur.execute(sql_login)
    login_data_res = cur.fetchall()
    data_packet = {"appKey":appKey,\
                    "groupId":groupId,\
                    "serverType":13,\
                    "serverId":cfg_global['localid'],\
                    "serverName":cfg_global['localname'].decode('gbk'),\
                    "appEvents":[],\
                   }

    login_event_cnt = 0
    create_role_event_cnt = 0
    pay_event_cnt = 0
    for res_one in login_data_res:
        t_info = res_one['log_info'].split(';')
        ip = ''
        if(len(t_info)<2):
        	print 'error_log:'+res_one['user_account']
        else:
        	ip_info = t_info[1].split(':');
        	if(len(ip_info)<2):
        		print 'error_log:'+res_one['user_account']
        	else:
        		ip = ip_info[1]
        #-------------登录事件
        if res_one['op_type']==1006 or res_one['op_type']==1002:
            #都是登录成功，失败没有记
            login_result = 0
            #http req发到数据中心去
            user_event_data = {"id":4,\
                                "label":"login",\
                                #标准时，转北京时间
                                "startTime":int((res_one['param2']-28800)*1000),\
                                "msgType":2,\
                                "appProfile":{"appVersionCode":"",\
                                            "appVersionName":"",\
                                            "partnerId":"",\
                                            "appType":12\
                                            },\
                                "deviceProfile": {"deviceId":"",\
                                            "ip":ip,\
                                            },\
                                "parameters":{"type":login_result,\
                                            "userName":(res_one['user_account']).lower(),\
                                            "userType":"",\
                                            "userLev":int(res_one['user_level']),\
                                            "vipLev":int(res_one['param3']),\
                                            "areaName":cfg_global['localname'].decode('gbk'),\
                                            },\
                                }
            data_packet["appEvents"].append(user_event_data)
            login_event_cnt+=1
        #--------------创角事件
        else:
            user_event_data = {"id":6,\
                                "label":"register",\
                                "startTime":int((res_one['param2']-28800)*1000),\
                                "msgType":2,\
                                "appProfile":{"appVersionCode":"",\
                                             "appVersionName":"",\
                                             "partnerId":"",\
                                             "appType":12\
                                              },\
                                "deviceProfile": {"deviceId":"",\
                                             "ip":ip,\
                                             },\
                                "parameters":{"userName":(res_one['user_account']).lower(),\
                                              "userType":"",\
                                              "areaName":cfg_global['localname'].decode('gbk'),\
                                              "clientIp":ip,\
                                              },\
                                }
            data_packet["appEvents"].append(user_event_data)
            create_role_event_cnt+=1
        #满1000个事件，直接发掉，避免单个包太大
        if(len(data_packet["appEvents"])>=1000):
            send_packet(data_packet)
            data_packet["appEvents"]=[]

    #-----------从数据库查充值数据
    today_zero_dt = datetime.datetime(now_tm.tm_year,now_tm.tm_mon,now_tm.tm_mday)
    today_zero_timestamp = time.mktime(today_zero_dt.timetuple())
    now_time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(today_zero_timestamp))
    last_day_time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(today_zero_timestamp-86400))
    
    conn = MySQLdb.connect(host=cfg_global['db_host'],user=cfg_global['db_user'],db=cfg_global['db_name_bs_log'],passwd=cfg_global['db_passwd'],charset=cfg_global['db_charset'])
    cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    temp_sql = "SELECT * FROM `tblrecharge_%d` where OpTime >\'%s\' and OpTime<=\'%s\'"
    for i in range(0,10):
        real_sql = temp_sql % (i,last_day_time_str,now_time_str)
        cur.execute(real_sql)
        results = cur.fetchall()
        for res_one in results:
            recharge_yb_cnt = int(res_one['rechybcount'])
            op_time = time.mktime(res_one['OpTime'].timetuple())
            user_event_data = {"id":14,\
                                "label":"rmbRecharge",\
                                "startTime":int(op_time*1000),\
                                "msgType":2,\
                                "appProfile":{"appVersionCode":"",\
                                              "appVersionName":"",\
                                              "partnerId":"",\
                                              "appType":12\
                                              },\
                                "parameters":{"userName":(res_one['UserAccount']).lower(),\
                                              "userType":"",\
                                              "sellPrice":res_one['rmbcount']/100,\
                                              "cardPrice":recharge_yb_cnt/10,\
                                              "cardValue":recharge_yb_cnt,\
                                              "orderId":res_one['OpOrder'],\
                                              "areaName":cfg_global['localname'].decode('gbk'),\
                                              "rechargeType":res_one['bstype'],
                                              },\
                                }
            data_packet["appEvents"].append(user_event_data)
            pay_event_cnt+=1
            #满1000个事件，直接发掉，避免单个包太大
            if(len(data_packet["appEvents"])>=1000):
                send_packet(data_packet)
                data_packet["appEvents"]=[]
                
    #-----------从数据库查在线数据
    conn = MySQLdb.connect(host=cfg_global['db_host'],user=cfg_global['db_user'],db=cfg_global['db_name_game'],passwd=cfg_global['db_passwd'],charset=cfg_global['db_charset'])
    cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    temp_sql = "SELECT * FROM `tdatastatis_level` where updatetime >\'%s\' and updatetime<=\'%s\'"% (last_day_time_str,now_time_str)
    cur.execute(temp_sql)
    results = cur.fetchall()
    for res_one in results:
        op_time = time.mktime(res_one['updatetime'].timetuple())
        level_infos = res_one['levelinfo'].split(';')
        total_cnt = 0
        for level_one in level_infos:
            if(level_one):
                cnt_info = level_one.split(',')
                if(len(cnt_info)==2):
                    total_cnt+=int(cnt_info[1])
        user_event_data = {"id":56,\
                            "label":"userOnline",\
                            "startTime":int(op_time*1000),\
                            "msgType":2,\
                            "appProfile":{"appVersionCode":"",\
                                          "appVersionName":"",\
                                          "partnerId":"",\
                                          "appType":12\
                                          },\
                            "parameters":{"areaName":cfg_global['localname'].decode('gbk'),\
                                          "count":total_cnt
                                          },\
                            }
        data_packet["appEvents"].append(user_event_data)
        if(len(data_packet["appEvents"])>=1000):
            send_packet(data_packet)
            data_packet["appEvents"]=[]
    #把剩下的事件都发掉
    send_packet(data_packet)
    print "login event:"+str(login_event_cnt)+",create role event:"+str(create_role_event_cnt)+",pay event:"+str(pay_event_cnt)
    
def send_packet(send_data):
    print "send_packet,event count:"+str(len(send_data["appEvents"])) 
    send_data_json = json.dumps(send_data,sort_keys=True,indent=4)
    conn = httplib.HTTPConnection("ykdc.hzyoka.com:80")    
    conn.request("POST", "/bfrd/json", send_data_json)    
    response = conn.getresponse()
    print response.read()

def main():
    #读取游戏服务器配置
    with open('../config.ini','r') as f_cfg:
        cfg_data = f_cfg.read()
        cfg_array = cfg_data.split('\n')
        for c in cfg_array:
            if(c.find('=')>=0):
                c_obj = c.split('=');
                cfg_global[str(c_obj[0]).strip()] = str(c_obj[1]).strip()

    #进入循环任务
    cur_time = time.time()
    cur_tm = time.localtime(cur_time)
    today_zero_dt = datetime.datetime(cur_tm.tm_year,cur_tm.tm_mon,cur_tm.tm_mday)
    today_zero_timestamp = time.mktime(today_zero_dt.timetuple())

    #凌晨0点10分提交数据
    if(cur_tm.tm_hour==1 and cur_tm.tm_min<10):
        delay_time = 600 - (cur_time - today_zero_timestamp)
    else:
        delay_time = 600 - (cur_time - today_zero_timestamp) + 86400
    s.enter(delay_time,0,sched_func,(86400,))
    #print "delay_time:"+str(delay_time)
    #test
    #s.enter(0,0,sched_func,(86400,))
    s.run()

if __name__ == "__main__":
    main()
