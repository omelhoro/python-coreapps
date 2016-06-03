'''
Created on Apr 23, 2014

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
    command_dct={"sleep":sleep_wrap}
    while True:
        data = ss.recv(1024)
        if not data: break
        mess=data.split()
        print_mess=lambda: data
        f=command_dct.get(mess[0],print_mess)
        if f.__name__=="sleep_wrap":
            f=f(int(mess[1]))
        f()

def sleep_wrap(t):
    def sleep():
        import time
        print(t)
        time.sleep(t)
        print("wake up")
    return sleep


Thread(target=recv).start()
while True:
    data = raw_input(">")
    if not data: break
    ss.send(data)

ss.close()

