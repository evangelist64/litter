import MySQLdb
import os,sys
import time

os.chdir(os.path.dirname(sys.argv[0]))

db_host='127.0.0.1'
db_user='root'
db_passwd=''
db_name='shuangqserverdb1'
db_charset='utf8'

def do_query():
        try:
                conn = MySQLdb.connect(host=db_host,user=db_user,db=db_name,passwd=db_passwd,charset=db_charset)
                cur = conn.cursor()

                f = open('aa.csv','w')
                sql_1 = 'SELECT * FROM `ljsusers`'
                cur.execute(sql_1)
                results = cur.fetchall()
                for r in results:
                        f.write(str(r[0]))
                        f.write(",")
                        f.write(str(r[1]))
                        f.write(",")
                        f.write(str(r[2]))
                        f.write(",")
                        f.write('\n')
                f.close()
                cur.close()
                conn.close()
        except MySQLdb.Error,e:
                print "error %d:%s" % (e.args[0],e.args[1])


do_query()
