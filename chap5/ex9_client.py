'''
Created on May 18, 2014

@author: igor
'''
import socket
from threading import Thread
from Tkinter import Tk, Text, Label, StringVar, Button
from time import ctime
from sys import maxint
from random import randint
from Tkconstants import END
import sys
from _socket import SHUT_RDWR

HOST="localhost"
PORT=49999
class ClientView(object):
    
    def __init__(self,HOST="localhost",PORT=49999):
        self.top=Tk()
        self.dialog=StringVar()
        self.user_pool=StringVar()
        self.name=StringVar()
        
        self.dialog_label=Label(self.top,text=ctime(randint(0,maxint)))
        self.user_pool_field=Label(self.top,text=self.user_pool)
        self.input_field=Text(self.top)
        self.name_field=Text(self.top,height=1,width=10)
        self.send=Button(self.top,text="Send",command=self.send_input)
        self.send_n=Button(self.top,text="Send",command=self.send_newname)
        self.exit=Button(self.top,text="Quit", command=self.exit)
        
        self.cs=socket.socket()
        self.cs.connect((HOST,PORT))
        
        fields=[self.dialog_label,self.input_field,self.send,self.user_pool_field,self.name_field,self.send_n,self.exit]
        [x.pack() for x in fields]
        Thread(target=self.recv).start()
        self.top.mainloop()


    def exit(self):
        print("exit1")
        self.cs.send("ext/abc")
        self.cs.shutdown(SHUT_RDWR)
        self.top.quit()
        print("exit2")

    def send_input(self):
        data=self.input_field.get("0.0",END)
        self.cs.send("mes/"+data)
        self.input_field.delete("0.0",END)
    
    def send_newname(self):
        data=(self.name_field.get("0.0",END)).strip()
        print(data)
        self.cs.send("nme/"+data.strip())
    
    def recv(self):
        while True:
            data = self.cs.recv(1024)
            if not data: break
            modus,mes=data[:4],data[4:]
            print(data)
            if modus=="mes/" or modus=="sta/":
                self.dialog.set(self.dialog.get()+mes)
                self.dialog_label.config(text=self.dialog.get())
            elif modus=="usr/":
                self.user_pool.set(mes)
                self.user_pool_field.config(text=self.user_pool.get())

ClientView()
