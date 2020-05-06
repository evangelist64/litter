import os,sys

os.chdir(os.path.dirname(sys.argv[0]))

f=open('ff.txt','rb')
f.seek(0,0)
index=0
for i in range(0,16):
	print "%3s" % hex(i),
print
for i in range(0,16):
	print "%-3s" % "#",
print
while True:
	temp=f.read(1)
	if len(temp) == 0:
		break
	else:
		print "%3s" % temp.encode('hex'),
		index=index+1
	if index == 16:
		index=0
		print 
f.close()