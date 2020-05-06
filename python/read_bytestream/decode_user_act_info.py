import os,sys
import struct
 
os.chdir(os.path.dirname(sys.argv[0]))

def decode_player_info():
    with open('ff.txt','rb') as f:
        data = f.read()
        length = len(data)
        compensation = struct.unpack('c',data[length-1:length])[0]
        print ord(compensation)

decode_player_info()
