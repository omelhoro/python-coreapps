'''
Created on Apr 16, 2014

@author: igor
'''
#from thread import start_new_thread
#===============================================================================
# from multiprocessing import Process
# import socket as s
# HOST="localhost"
# PORT=49999
# 
# def listen():
#     print("hihihih")
#     mess=ss.recv(0)
#     print(mess)
# 
# def talk():
#     print("huhuhu")
#     mess=raw_input("User: ")
#     ss.sendall(mess)
# 
# ss=s.socket()
# ss.connect((HOST,PORT))
# 
# l=Process(target=listen)
# t=Process(target=talk)
# 
# while True:
#     l.run()
#     t.run()
#===============================================================================

#===============================================================================
# while True:
#     start_new_thread(listen,(1,))
#     start_new_thread(talk,(1,))
#===============================================================================

#===============================================================================
# while True:
#     mess=raw_input("User: ")
#     ss.sendall(mess)
#===============================================================================
    #start_new_thread(talk,(1,))
#===============================================================================
# import asyncore
# import socket
# 
# 
# class Chatter(asyncore.dispatcher):
#     # time requestor (as defined in RFC 868)
# 
#     def __init__(self, host="localhost", port=49999):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.connect((host, port))
# 
#     def handle_write(self):
#         mess=raw_input("User: ")
#         self.send(mess)
# 
#     def handle_connect(self):
#         pass # connection succeeded
# 
#     def handle_expt(self):
#         self.close() # connection failed, shutdown
# 
#     def handle_read(self):
#         d=self.recv(1024)
#         print(d)
# 
#     def handle_close(self):
#         self.close()
# 
#     def adjust_time(self, delta):
#         # override this method!
#         print "time difference is", delta
# 
# #
# # try it out
# 
# request = Chatter()
# 
# asyncore.loop()
#===============================================================================
from socket import *
from threading import Thread
import sys

HOST = 'localhost'
PORT = 49999
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

def recv():
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        if not data: sys.exit(0)
        print(data)

Thread(target=recv).start()
while True:
    data = raw_input()
    if not data: break
    tcpCliSock.send("\n"+"User: "+data)

tcpCliSock.close()
