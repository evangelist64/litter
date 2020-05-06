import os,sys
import re

os.chdir(os.path.dirname(sys.argv[0]))

with open('hu_today.txt','r') as f:
	f_str = f.read()
data_list = re.findall(r'\"(.*)\"',f_str)

with open('hu_all.txt','w') as f:
	for item in data_list:
		f.write(item+'\n')
