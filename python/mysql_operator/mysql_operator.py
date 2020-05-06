import MySQLdb
import os,sys
import time

os.chdir(os.path.dirname(sys.argv[0]))

#db_host='61.147.165.13'
db_host='10.225.10.60'
#db_user='byxmz'
db_user='root'
#db_passwd='sp2nm0qmf3d9EEeO'
db_passwd='sys731!@#'
db_name_log='sgs_log'
db_name_game='sgs_new'
db_charset='utf8'

yuanbao_table_name = 'tbl_goods_20151113'

exp_table_name = 'tbl_goods_20151113'

player_time_begin = '2015-11-10'
player_time_end = '2015-11-15'

vip_online_table_name = 'tbl_login_20151113'
vip_yuanbao_table_name = 'tbl_goods_20151113'

def get_yuanbao_log(is_recharge):
        try:
                print 'get yuanbao log begin...'
                conn = MySQLdb.connect(host=db_host,user=db_user,db=db_name_log,passwd=db_passwd,charset=db_charset)
                cur = conn.cursor()
                yuanbao_sum = {}
                yuanbao_time = {}
                yuanbao_people = {}
                type_list = [3,5,8,9,12,28,62,79,59,58,20,45,78,77,61,63]
                #print time.strftime('%Y%m%d',time.localtime(time.time()))
                if(is_recharge is False):
                        f = open('log_yuanbao.csv','w')
                        type_str = '(op_type = 6002 OR op_type = 1902)'
                else:
                        f = open('log_yuanbao_recharge.csv','w')
                        type_str = 'op_type = 1902'
                        
                sql_1 = 'SELECT SUM(param3) FROM `%s` WHERE %s AND param2 = %d;'
                sql_2 = 'SELECT COUNT(*) FROM `%s` WHERE %s AND param2 = %d;'
                sql_3 = 'SELECT COUNT(*) FROM (SELECT * FROM `%s` WHERE %s AND param2 = %d GROUP BY user_account) as a;'
                for i in type_list:
                        real_sql_1 = sql_1 % (yuanbao_table_name,type_str,i)
                        cur.execute(real_sql_1)
                        results = cur.fetchall()
                        for r in results:
                                yuanbao_sum[i] = 0 if (r[0] is None) else r[0]
                        real_sql_2 = sql_2 % (yuanbao_table_name,type_str,i)
                        cur.execute(real_sql_2)
                        results = cur.fetchall()
                        for r in results:
                                yuanbao_time[i] = 0 if (r[0] is None) else r[0]
                        real_sql_3 = sql_3 % (yuanbao_table_name,type_str,i)
                        cur.execute(real_sql_3)
                        results = cur.fetchall()
                        for r in results:
                                yuanbao_people[i] = 0 if (r[0] is None) else r[0]
                f.write('total,consume_time,player_count\n')
                for i in type_list:
                        f.write(str(yuanbao_sum[i]))
                        f.write(",")
                        f.write(str(yuanbao_time[i]))
                        f.write(",")
                        f.write(str(yuanbao_people[i]))
                        f.write(",\n")
                f.close()
                cur.close()
                conn.close()
                print 'get yuanbao log end'
        except MySQLdb.Error,e:
                print "error %d:%s" % (e.args[0],e.args[1])

def get_exp_log():
        try:
                print 'get exp log begin...'
                conn = MySQLdb.connect(host=db_host,user=db_user,db=db_name_log,passwd=db_passwd,charset=db_charset)
                cur = conn.cursor()
                exp_info = {}
                f = open('log_exp.csv','w')
                sql = "SELECT user_account,user_level,param2,param4,param3 FROM `%s` WHERE op_type = 6004"
                sql = sql % (exp_table_name)
                cur.execute(sql)
                results = cur.fetchall()
                f.write('user_accout,user_level,type,id,value\n')
                for r in results:
                        f.write(str(r[0]))
                        f.write(",")
                        f.write(str(r[1]))
                        f.write(",")
                        f.write(str(r[2]))
                        f.write(",")
                        f.write(str(r[3]))
                        f.write(",")
                        f.write(str(r[4]))
                        f.write(",\n")
                f.close()
                cur.close()
                conn.close()
                print 'get exp log end'
        except MySQLdb.Error,e:
                print "error %d:%s" % (e.args[0],e.args[1])

def get_player_log():
        try:
                print 'get player log begin...'
                conn = MySQLdb.connect(host=db_host,user=db_user,db=db_name_game,passwd=db_passwd,charset=db_charset)
                cur = conn.cursor()
                player_info = {}
                f = open('log_player_count.csv','w')
                sql = "SELECT * FROM tdatastatis_level WHERE updatetime >= '%s' AND updatetime < '%s' "
                sql = sql % (player_time_begin,player_time_end)
                cur.execute(sql)
                results = cur.fetchall()
                f.write('time,num\n')
                for r in results:
                        info_str = r[1]
                        split_levels = info_str.split(';')
                        player_cnt = 0
                        for cell_level in split_levels:
                                split_player = cell_level.split(',')
                                if(len(split_player) == 2):
                                        player_cnt += int(split_player[1])
                        f.write(str(r[0]))
                        f.write(",")
                        f.write(str(player_cnt))
                        f.write(",\n")
                f.close()
                cur.close()
                conn.close()
                print 'get player log end'
        except MySQLdb.Error,e:
                print "error %d:%s" % (e.args[0],e.args[1])

def get_vip_online_log():
        try:
                print 'get vip online log begin...'
                conn = MySQLdb.connect(host=db_host,user=db_user,db=db_name_log,passwd=db_passwd,charset=db_charset)
                cur = conn.cursor()
                vip_info = {}
                f = open('log_vip_online.csv','w')
                sql = "SELECT user_account,param3,op_type,param2 FROM %s WHERE (op_type = 1002 OR op_type = 1003 OR op_type = 1004) AND param3>=8 order by param2 asc"
                sql = sql % (vip_online_table_name)
                cur.execute(sql)
                results = cur.fetchall()
                f.write('user_accout,vip,type,time\n')
                for r in results:
                        f.write(str(r[0]))
                        f.write(",")
                        f.write(str(r[1]))
                        f.write(",")
                        f.write(str(r[2]))
                        f.write(",")
                        f.write(str(r[3]))
                        f.write(",\n")
                f.close()
                cur.close()
                conn.close()
                print 'get vip online log end'
        except MySQLdb.Error,e:
                print "error %d:%s" % (e.args[0],e.args[1])

def get_vip_yuanbao_log():
        try:
                print 'get vip yuanbao log begin...'
                conn = MySQLdb.connect(host=db_host,user=db_user,db=db_name_log,passwd=db_passwd,charset=db_charset)
                cur = conn.cursor()
                vip_info = {}
                f = open('log_vip_yuanbao.csv','w')
                sql_sub = "SELECT user_account, param4, SUM(param3) FROM %s WHERE (op_type = 6002 OR op_type = 1902) AND param4>=8 GROUP BY user_account"
                sql_add = "SELECT user_account, param4, SUM(param3) FROM %s WHERE (op_type = 6008 OR op_type = 1903) AND param4>=8 GROUP BY user_account"
                sql_sub = sql_sub % (vip_yuanbao_table_name)
                sql_add = sql_add % (vip_yuanbao_table_name)
                cur.execute(sql_sub)
                results = cur.fetchall()
                f.write('user_account,vip,type,value\n')
                for r in results:
                        f.write(str(r[0]))
                        f.write(",")
                        f.write(str(r[1]))
                        f.write(",")
                        f.write(str(r[2]))
                        f.write(",")
                        f.write(str(r[3]))
                        f.write(",\n")
                cur.execute(sql_add)
                results = cur.fetchall()
                for r in results:
                        f.write(str(r[0]))
                        f.write(",")
                        f.write(str(r[1]))
                        f.write(",")
                        f.write(str(r[2]))
                        f.write(",")
                        f.write(str(r[3]))
                        f.write(",\n")
                f.close()
                cur.close()
                conn.close()
                print 'get vip yuanbao log end'
        except MySQLdb.Error,e:
                print "error %d:%s" % (e.args[0],e.args[1])

                
#get_yuanbao_log(True)
#get_yuanbao_log(False)
#get_exp_log()
#get_player_log()
get_vip_online_log()
#get_vip_yuanbao_log()
