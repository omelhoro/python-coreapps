'''
Created on Apr 21, 2014

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

conns=[ss]

def recv(cs):
    while True:
        data = cs.recv(1024)
        print(data)
        if data :
            for co in conns[1:]:
                if co!=cs:
                    co.sendall(data)
        else:
            break

#Thread(target=accept).start()
while True:
    print(conns)
    conn,_=ss.accept()
    conns.append(conn)
    Thread(target=recv,args=(conn,)).start()
#pass

ss.close()

#%timeit li=range(1000);li=li+[1]
#%timeit li=range(1000);li.append(1)

