'''
Created on Apr 16, 2014

@author: igor
'''
import socket as s

HOST="localhost"
PORT=49999
ADDRESS=(HOST,PORT)

ss=s.socket()
ss.connect(ADDRESS)
while True:
    mess=raw_input("User: ")
    if not mess: break
    ss.sendall(mess)
    resp=ss.recv(1024)
    print(resp)
ss.close()