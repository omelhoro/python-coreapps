'''
Created on Apr 14, 2014

@author: igor
'''
#!/usr/bin/env python

from socket import *

#HOST = 'localhost'
#PORT = 21567

host_byuser=raw_input("Host: ")
port_byuser=raw_input("Port: ")
HOST= host_byuser if host_byuser else "localhost"
PORT= port_byuser if port_byuser else 21567

BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = raw_input('> ')
    if not data:
        break
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print data

tcpCliSock.close()