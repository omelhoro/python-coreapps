'''
Created on Apr 23, 2014

@author: igor
'''
import socket as s

#HOST="www.time.gov"
#HOST="www.faz.net"
HOST="stackoverflow.com"
HOST="stackexchange.com"
PORT=80

ss=s.socket()
ss.connect((HOST,PORT))

ss.send("GET /\n")
while True:
    data=ss.recv(4096)
    if not data: break
    print(data)
    