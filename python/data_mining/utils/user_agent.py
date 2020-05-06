import urllib2 
import os,sys

def grabData(url,save_file):
	response = urllib2.urlopen(url) 
	html = response.read() 
	with open(save_file,'w') as f:
		f.write(html)

if __name__=='__main__':
	os.chdir(os.path.dirname(sys.argv[0]))
	url = 'http://bbs.10jqka.com.cn/codelist.html'
	save_file = 'data.txt'
	grabData(url,save_file)
