# -*- coding:utf-8 -*-  

import os,sys
import regex as re

os.chdir(os.path.dirname(sys.argv[0]))

f = open('a.txt','r')

p1=','
p2='.*=.*([0-9*]).*'
p3='.*,.*'
a = 1

for line in f.read().splitlines():
    if not re.match(p2, line):
        if re.match(p3, line):
            out = re.sub(p1, '='+str(a)+';', line)
            print out
            a += 1
        else:
            print line
    else:
        a = int(re.match(p2, line).groups()[0])
        a += 1
        out = re.sub(p1, ';', line)
        print out
f.close()
