'''
Created on Apr 16, 2014

@author: igor
'''
HOST=""
PORT=49999
ADDRESS=(HOST,PORT)

import socket as s


ss=s.socket()
ss.bind(ADDRESS)
ss.listen(5)
print("Listening")

while True:
    conn,port=ss.accept()
    print("Connected from {}".format(port))
    while True:
        mess=conn.recv(1024)
        if not mess: break
        print(mess)
        resp=raw_input("Server: ")
        conn.sendall(resp)
print("End connection")
conn.close()