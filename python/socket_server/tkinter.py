from Tkinter import *
import struct
import socket
import threading
import ctypes
import tkMessageBox
from copy import deepcopy

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
	self.master.title('test')
	self.master.geometry('600x600')
	self.pack()

	self.cur_proc = []
	self.cur_proc_str = StringVar()
	self.cur_proc_struct = '='
	self.cur_struct_str = StringVar()

	self.all_proc_struct = ('=iiiHH48s48s48sHH?')
	self.all_proc = ([20201,1,0,1,1,1,'fff','','',0,0,True])

	self.all_proc_str = StringVar()
	self.createWidgets()
	self.connectToServer()

    def createWidgets(self):
	frm_L = Frame(self)
	frm_L.pack(side = LEFT)
	
	self.entry_int = Entry(frm_L)
	self.entry_int.pack()
	self.button_str = Button(frm_L,text="writeInt",command=self.writeInt)
	self.button_str.pack()

	self.entry_int = Entry(frm_L)
	self.entry_int.pack()
	self.button_str = Button(frm_L,text="writeStr",command=self.writeStr)
	self.button_str.pack()

	self.cur_proc_label = Label(frm_L,textvariable=self.cur_proc_str)
	self.cur_proc_label.pack(pady=10)

	frm_R = Frame(self)
	frm_R.pack(side = RIGHT,padx=80)

	self.button_clear = Button(frm_R,text="clearProc",command=self.clearProc)
	self.button_clear.pack(pady=10)

	self.button_send = Button(frm_R,text="sendProc",command=self.sendProc)
	self.button_send.pack(pady=10)

	self.all_proc_lb = Listbox(frm_R,listvariable=self.all_proc_str,width=200,height=200)
	self.all_proc_lb.bind('<ButtonRelease-1>',self.selectProc)
	self.all_proc_lb.pack(pady=10)
	self.all_proc_str.set(self.all_proc)

	self.updateView()

def connectToServer(self):
	print 'connect to server...'
	try:
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print self.sock.conncet("101.37.19.208",41111)
	except socket.error,msg:
		print 'error'+str(msg)
		sys.exit()

	self.t = threading.Thread(target=self.listenReply)
	self.t.start()

def listenReply(self):
	while 1:
		recv_data = self.sock.rect(1024)
		print recv_data
		recv_file = open('E:/rect.txt','w')
		recv_file.write(recv_data)
		recv_file.close()

		if not recv_data:
			break

def selectProc(self,event):
	idx= self.all_proc_lb.curselection()[0]
	self.cur_proc_struct = self.all_proc_struct[idx]
	self.cur_proc = deepcopy(self.all_proc[idx])

	self.updateView()

def writeInt(self):
	input_int = int(self.entry_int.get())
	self.cur_proc.append(input_int)
	self.cur_proc_struct += self.getTypeDesc(input_int)
	self.entry_int.delete(0,len(self.entry_int.get()))

	self.updateView()

def writeString(self):
	input_str = int(self.entry_str.get())
	self.cur_proc.append(input_str)
	self.cur_proc_struct += self.getTypeDesc(input_str)
	self.entry_int.delete(0,len(self.entry_str.get()))

	self.updateView()

def clearProc(self):
	self.cur_proc=[]
	self.cur_proc_struct=''
	self.updateView()

def sendProc(self):
	s = struct.Struct(self.cur_proc_struct)
	prebuffer = ctypes.create_string_buffer(s.size)
	s.pack_into(prebuffer,0,*self.cur_proc)

	print s.unpack_from(prebuffer,0)
	self.sock.send(prebuffer)

def updateView(self):
	self.cur_proc_str.set(self.cur_proc)
	self.cur_struct_str.set(self.cur_proc_struct)

def getTypeDesc(self,data):
	if(isinstance(data,int)):
		return 'i'
	elif(isinstance(data,str)):
		return str(len(data))+'s'
	else:
		tkMessageBox.showinfo('Message','not supported data type')
		return ''

app = Application()
app.mainloop()
