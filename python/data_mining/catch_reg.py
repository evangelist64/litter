import os,sys
import re
import urllib2 
import utils.user_agent

os.chdir(os.path.dirname(sys.argv[0]))

with open('hu.txt') as f:
	f_str = f.read()

id_list = re.findall(r"([0-9][0-9][0-9][0-9][0-9][0-9])<",f_str)

f = open('hu_today.txt','w')

for id in id_list:
	url = 'http://hq.sinajs.cn/list=sh%s' % id
	response = urllib2.urlopen(url)
	html = response.read() 
	f.write(html)
f.close()
