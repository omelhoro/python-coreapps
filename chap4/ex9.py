'''
Created on May 7, 2014

@author: igor
'''
import os
from Queue import Queue
from MyThread import MyThread
import cProfile

path="/home/igor/Downloads/large_files/"
fls=[path+fl for fl in os.listdir(path)]

def prepare_queue(queue_size):
    q=Queue(queue_size)
    step=sum(os.path.getsize(fl) for fl in fls)/queue_size
    for fl in fls:
        size=os.path.getsize(fl)
        for r in xrange(0,size,step):
            if q.qsize()!=queue_size:
                q.put((fl,r))
    return q,step

def thr_count_lines(n_threads=5):

    def counter(a):
        while q.qsize()!=0:
            fl,r=q.get(1)
            print("Start with {0} line {1}".format(fl,r))
            with open(fl) as f:
                f.seek(r)
                mid_results.append(len(f.readlines(step)))
        
    q,step=prepare_queue(32)
    print(q,step)
    mid_results=[]
    threads= [MyThread(counter,(step,)) for _ in range(n_threads)]
    [thr.start() for thr in threads]
    [thr.join() for thr in threads]
    print(sum(mid_results))
    

def sin_count_lines():
    q,step=prepare_queue(32)
    tot_lns=0
    while q.qsize()!=0:
        fl,r=q.get(1)
        print(fl,r)
        with open(fl) as f:
            f.seek(r)
            tot_lns+=len(f.readlines(step))
    print(tot_lns)

print(cProfile.run("thr_count_lines()"))
print(cProfile.run("thr_count_lines(10)"))
print(cProfile.run("sin_count_lines()"))



