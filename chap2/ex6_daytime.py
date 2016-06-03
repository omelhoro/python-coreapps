import socket
import os
import time

import socket
#from _socket import getservbyname

#===============================================================================
# HOST = 'localhost'    # The remote host
# PORT = socket.getservbyname("daytime")              # The same port as used by the server
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# print(HOST,PORT)
# s.connect(("time.nist.gov", PORT))
# #with s.makefile() as f:
# #    print(f.read())
# #b=s.makefile()
# data = s.recv(1024)
# print('Received', data,repr(data))
# s.close()
#===============================================================================
#
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "time.nist.gov"
port = 13
s.connect((host,port))
while True:
    data = s.recv(10000)
    if data:
        print data
    else:
        break

s.close()

#===============================================================================
# import socket
# from contextlib import closing as C
# 
# address = "time.nist.gov", socket.getservbyname('daytime')
# 
# with C(socket.create_connection(address, timeout=2)) as conn:
#     with C(conn.makefile()) as f:
#          print f.read(),
#===============================================================================