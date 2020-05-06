import os,sys
import struct
 
os.chdir(os.path.dirname(sys.argv[0]))

def decode_mail_info():
    with open('ff.txt','rb') as f:
        version = f.read(4)
        print 'version:%s'%struct.unpack('l',version)[0]
        verify = f.read(4)
        print 'verify:%s'%struct.unpack('l',verify)[0]
        data_len = f.read(4)
        print 'data_len:%s'%struct.unpack('l',data_len)[0]

        body_len_stream = f.read(2)
        body_len = struct.unpack('H',body_len_stream)[0]
        print 'body_len:%s'%body_len

        body = f.read(body_len)
        acc_num_stream = f.read(1)
        acc_num = ord(struct.unpack('c',acc_num_stream)[0])
        print 'acc_num:%s'%acc_num
        for i in range(1,acc_num+1):
            good_id = f.read(4)
            good_num = f.read(4)
            print 'good_id:%s,good_num:%s'%(struct.unpack('l',good_id)[0],struct.unpack('l',good_num)[0])

decode_mail_info()
