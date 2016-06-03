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

rooms={
       "linux":[],
       "backing":[],
       "football":[]
       }

def recv(cs):
    invalid=True
    while invalid:
        print("input")
        cs.sendall("\n".join([str(i+1)+k for i,k in enumerate(rooms.keys())]))
        choice=cs.recv(1024)
        choice_index=int(choice)-1
        choice_key=rooms.keys()[choice_index]
        rooms[choice_key].append(conn)
        invalid=False
    print(rooms[choice_key])
    while True:
        data = cs.recv(1024)
        print(data)
        if data :
            for co in rooms[choice_key]:
                if co!=cs:
                    co.sendall(data)
        else:
            break

#Thread(target=accept).start()
while True:
    conn,_=ss.accept()
    print(rooms)
    Thread(target=recv,args=(conn,)).start()
#pass

ss.close()
