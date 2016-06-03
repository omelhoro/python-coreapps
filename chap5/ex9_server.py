'''
Created on May 18, 2014

@author: igor
'''
from socket import socket
from threading import Thread
from random import randint

HOST="localhost"
PORT=49999

server=socket()
server.bind((HOST,PORT))
server.listen(5)

client_pool=[]
filtered_pool=lambda: filter(lambda x: x[0] ,client_pool)

def recv_client(cs,i):
    while True:
        try:
            message=cs.recv(1024)
            if not message: break
            modus,mes=message[:4],message[4:]
            print("dort",message,client_pool)
            if modus=="mes/":
                for conn,_ in filtered_pool():
                    conn.sendall("mes/{name}: {mes}".format(name=client_pool[i][1],mes=mes))
            elif modus=="nme/":
                client_pool[i]=(cs,mes)
                update_user_pool()
            elif modus=="ext/":
                client_pool[i]=("","")
                transmit_changed_status(cs, client_pool[i][1])
                update_user_pool()
                break
        except:
            break
            

def transmit_changed_status(changed_conn,nm):
    for conn,_ in filtered_pool():
        if conn!=changed_conn:
            conn.sendall("sta/Server: {nm} has left the chatroom.\n".format(nm=nm))
    

def update_user_pool():
    usr_status="usr/"+ "\n".join(zip(*filtered_pool())[1])
    print("user",usr_status)
    for conn,_ in filtered_pool():
        print "here",conn,_,usr_status,filtered_pool()
        conn.sendall(usr_status)

def main():
    while True:
        conn,_=server.accept()
        name="".join(map(chr, [randint(60,120) for _ in range(6)]))
        i=len(client_pool)
        client_pool.append((conn,name))
        Thread(target=recv_client,args=(conn,i)).start()
        print("tatt1",client_pool)
        update_user_pool()
        print("tatt",client_pool)
    server.close()

main()
