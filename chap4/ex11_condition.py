'''
Created on May 7, 2014

@author: igor
'''

from random import randint 
from threading import Condition
from time import sleep
from Queue import Queue
from MyThread import MyThread



    

def main():

    def writer(loops,name):
    
        def writeQ():
            with q:
                print 'producing object for Q...',
                q.notify()
        
        for _ in range(loops):
            sleep(randint(2, 3))
            writeQ()
    
    def reader(loops,name):
        for i in range(loops):
            with q:
                q.wait()
                print("Go on")
        
    
    nloops = randint(4, 5)
    q = Condition()
    funcs = [reader,writer]
    
    thread= lambda func,nm:MyThread(func, (nloops,nm), func.__name__) 
    threads = [ thread(f,i) for i,f in enumerate(funcs)]
    [thr.start() for thr in threads]
    [thr.join() for thr in threads]
    print 'all DONE'

if __name__ == '__main__':
    main()
