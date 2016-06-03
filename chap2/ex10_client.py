'''
Created on Apr 21, 2014

@author: igor
'''
import socket as s
from threading import Thread


PORT=49999
HOST=""
ADDRESS=(HOST,PORT,)

ss=s.socket()
ss.connect(ADDRESS)


def recv():
    while True:
        data = ss.recv(1024)
        if not data: break
        print(data+"\n")

Thread(target=recv).start()
choice=raw_input("Choice: ")
ss.send(choice)
name=raw_input("Your name: ")
while True:
    data = raw_input(">")
    if not data: break
    ss.send("\n"+name+": "+data)

ss.close()