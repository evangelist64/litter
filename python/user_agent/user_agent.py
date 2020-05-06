import urllib2
import os,sys
 
os.chdir(os.path.dirname(sys.argv[0]))

response = urllib2.urlopen('http://nba.hupu.com/') 
html = response.read() 
with open('fff.txt', 'w') as f:
    f.write(html)
