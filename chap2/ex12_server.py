'''
Created on Apr 23, 2014

@author: igor
'''
import socket as s
from threading import Thread


PORT=49999
HOST=""
ADDRESS=(HOST,PORT)
ss=s.socket()
ss.bind(ADDRESS)
ss.listen(5)

def recv(cs):
    while True:
        def put_to_sleep(tm=10):
            cs.send("sleep {}".format(tm))
        data=cs.recv(1024)
        print(data)
        command_dct={
                     "put_to_sleep":put_to_sleep
                     }
        mess=data.split()
        print_data=lambda : data
        f=command_dct.get(mess[0],print_data)
        f()


while True:
    conn,_=ss.accept()
    recv(conn)

ss.close()
