'''
Created on Apr 16, 2014

@author: igor
'''
#===============================================================================
# from multiprocessing import Process
# 
# #from thread import start_new_thread
# import socket as s
# HOST=""
# PORT=49999
# 
# ss=s.socket()
# ss.bind((HOST,PORT))
# ss.listen(5)
# 
# def listen(conn):
#     mess=conn.recv(1024)
#     print(mess)
# 
# def talk(conn):
#     res=raw_input("Server: ")
#     conn.sendall(res)        
# 
# while True:
#     conn,addr=ss.accept()
#     print(conn,addr)
#     l=Process(target=listen,args=(conn,))
#     t=Process(target=talk,args=(conn,))
#     l.start()
#     t.start()
#     
# ss.close()
#===============================================================================

#===============================================================================
# import asyncore
# import socket
# 
# class ServerChatter(asyncore.dispatcher):
#     def __int__(self,conn):
#         asyncore.dispatcher.__init__(self,sock=conn)
#         #self.conn=conn
# 
#     def handle_expt(self):
#         self.close() # connection failed, shutdown
# 
#     def handle_read(self):
#         #+d=self.recv(1024)
#         print(self.recv(1024)+"\n")
# 
#     def handle_write(self):
#         mess=raw_input("Server: ")
#         #sent = 
#         self.send(mess)
#         #self.buffer = self.buffer[sent:]
# 
#     def handle_close(self):
#         self.close()
# 
#     def adjust_time(self, delta):
#         # override this method!
#         print "time difference is", delta
# 
# 
# class Server(asyncore.dispatcher):
# 
#     def __init__(self, port=37):
#         asyncore.dispatcher.__init__(self)
#         self.port = port
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.bind(("", port))
#         self.listen(5)
#         print "listening on port", self.port
# 
#     def handle_expt(self):
#         self.close() # connection failed, shutdown
# 
#     def handle_close(self):
#         self.close()
# 
#     def handle_accept(self):
#         channel, addr = self.accept()
#         print(channel,addr)
#         ServerChatter(channel)
# 
# server = Server(49999)
# asyncore.loop()
#===============================================================================

#===============================================================================
# import asyncore
# import logging
# import socket
# 
# #from asynchat_echo_handler import EchoHandler
# 
# class Server(asyncore.dispatcher):
#     """Receives connections and establishes handlers for each client.
#     """
#     
#     def __init__(self, address):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.bind(("",49999))
#         self.address = self.socket.getsockname()
#         self.listen(1)
#         return
# 
#     def handle_accept(self):
#         # Called when a client connects to our socket
#         client_info = self.accept()
#         EchoHandler(sock=client_info[0])
#         # We only want to deal with one client at a time,
#         # so close as soon as we set up the handler.
#         # Normally you would not do this and the server
#         # would run forever or until it received instructions
#         # to stop.
#         self.handle_close()
#         return
#     
#     def handle_close(self):
#         self.close()
#         
# import asynchat
# import logging
# 
# class EchoHandler(asynchat.async_chat):
#     """Handles echoing messages from a single client.
#     """
# 
#     # Artificially reduce buffer sizes to illustrate
#     # sending and receiving partial messages.
#     ac_in_buffer_size = 64
#     ac_out_buffer_size = 64
#     
#     def __init__(self, sock):
#         self.received_data = []
#         self.logger = logging.getLogger('EchoHandler')
#         asynchat.async_chat.__init__(self, sock)
#         # Start looking for the ECHO command
#         self.process_data = self._process_command
#         self.set_terminator('\n')
#         return
# 
#     def collect_incoming_data(self, data):
#         """Read an incoming message from the client and put it into our outgoing queue."""
#         #self.logger.debug('collect_incoming_data() -> (%d bytes)\n"""%s"""', len(data), data)
#         print(data)
#         self.received_data.append(data)
# 
#     def found_terminator(self):
#         """The end of a command or message has been seen."""
#         self.logger.debug('found_terminator()')
#         self.process_data()
#     
#     def _process_command(self):        
#         """We have the full ECHO command"""
#         command = ''.join(self.received_data)
#         command_verb, command_arg = command.strip().split(' ')
#         expected_data_len = int(command_arg)
#         self.set_terminator(expected_data_len)
#         self.process_data = self._process_message
#         self.received_data = []
# 
#     def handle_write (self):
#         data=raw_input("Server: ")
#         self.push(data)
#     
#     def _process_message(self):
#         """We have read the entire message to be sent back to the client"""
#         to_echo = ''.join(self.received_data)
#         self.push(to_echo)
#         # Disconnect after sending the entire response
#         # since we only want to do one thing at a time
#         self.close_when_done()
# 
# server = Server(49999)
# asyncore.loop()
#===============================================================================

import socket as s
from threading import Thread
import sys

HOST=""
PORT=49999
 
ss=s.socket()
ss.bind((HOST,PORT))
ss.listen(5)
 
def listen(conn):
    while True:
        for c in conn:
            mess=c.recv(1024)
            print(mess)
 
def talk(conn):
    res=raw_input("Server: ")
    conn.sendall(res)        

def accept(a):
    while True:
        aa,b=ss.accept()
        print("hhhh",aa,a)
        return a.append(aa)
    
while True:
    conn=[]
    print(conn)
    Thread(target=accept,args=(conn,)).start()
    Thread(target=listen,args=(conn,)).start()
    while True:
        res=raw_input()
        for c in conn:
            print(conn)
            c.sendall("\n"+"Server: " +res)        
     
ss.close()

