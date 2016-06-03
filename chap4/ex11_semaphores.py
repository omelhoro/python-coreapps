'''
Created on May 12, 2014

@author: igor
'''
import threading as thd
from random import randint
from MyThread import MyThread

def main():
    alphab="asdnasdfvcboiopk;l;"
    randchar=lambda: alphab[randint(0,len(alphab)-1)]
    ressource=[randchar() for _ in range(10)]
    
    sem=thd.Semaphore(5)
    
    def reader(nloops):
        for _ in range(nloops):
            with sem:
                print(ressource[0])
    
    readers=[reader,reader,reader]
    threads=[MyThread(f,(5,)) for f in readers]
    [thr.start() for thr in threads]
    [thr.join() for thr in threads]
    print("Done")

main()
        
    