import urllib2
import os,sys
 
os.chdir(os.path.dirname(sys.argv[0]))

response = urllib2.urlopen('http://shuju.wdzj.com/') 
html = response.readline()
while(html):   
    print html
    html = response.readline()
#with open('fff.txt', 'w') as f:
#    f.write(html)
