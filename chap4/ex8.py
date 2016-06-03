'''
Created on May 7, 2014

@author: igor
'''
#!/usr/bin/env python

from random import randint
from time import sleep
from Queue import Queue
from MyThread import MyThread



def writer(queue, loops,name):

    def writeQ(queue):
        print 'producing object for Q...',
        queue.put('xxx', 1)
        print "size now", queue.qsize()
    
    for _ in range(loops):
        writeQ(queue)
        sleep(randint(1, 3)/10)

def reader(queue, loops,name):

    def readQ(queue):
        queue.get(randint(3,8))
        print '{} consumed object from Q... size now'.format(name),queue.qsize()
    
    for _ in range(loops):
        if queue.qsize()==0:
            break
        readQ(queue)
        sleep(randint(2, 5))


def main(n_readers=5):
    nloops = randint(20, 50)
    q = Queue(32)
    funcs = [writer]+ [reader]*n_readers
    
    thread= lambda func,nm:MyThread(func, (q, nloops,nm), func.__name__) 
    threads = [ thread(f,i) for i,f in enumerate(funcs)]
    [thr.start() for thr in threads]
    [thr.join() for thr in threads]
    print 'all DONE'

if __name__ == '__main__':
    main()
