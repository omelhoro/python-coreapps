'''
Created on Apr 14, 2014

@author: igor
'''
import socket
import os
import time

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        if not data: break
        data=data.strip().split()
        join_dirs= lambda x:",".join(os.listdir(x))
        list_dir=lambda :  join_dirs(data[1]) if len(data)>1 else join_dirs(os.curdir)
        commands={
                  "os":lambda: os.name,
                  "date":time.ctime,
                  "ls":list_dir
                  }
        com_not_found=lambda: "Command not found: {com}".format(com=data[0])
        resp_command=commands.get(data[0],com_not_found)
        conn.sendall(resp_command())
print("Close connection")
conn.close()
