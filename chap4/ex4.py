'''
Created on May 5, 2014

@author: igor
'''
import os
#from threading import Thread
from MyThread  import MyThread as Thread

def thr_count_bytes(val,flnm,n_threads=10):

    def count_byte(val,flnm="/home/igor/bin/praat-old",start=0,step=1024):
        with open(flnm,"rb") as f:
            f.seek(start)
            txt=f.read(step)
            return txt.count(val)
    
    flnm_size=range(0,os.path.getsize(flnm),os.path.getsize(flnm)/n_threads)
    step=os.path.getsize(flnm)/n_threads
    threads=[]
    for i in flnm_size:
        threads.append(Thread(count_byte,args=(val, flnm, i, step)))
    
    [th.start() for th in threads]
    [th.join() for th in threads]
    b=sum([th.getResult() for th in threads])
    print(b)
    return b


def sin_count_bytes(val,flnm):
    with open(flnm,"rb") as f:
        txt=f.read()
        return txt.count(val)

def singen_count_bytes(val,flnm):
    n_val=0
    with open(flnm,"rb") as f:
        for ln in f:
            n_val+=ln.count(val)
        return n_val

flnm="/home/igor/bin/praat-old"
flnm="/home/igor/Desktop/Link to Documents/eclipse_data/audio_2/15/Lesen/113212_ru_07_k.WAV"
flnm="/home/igor/Documents/eclipse_data/audio_2/11/Sprechen/112199_ru_04_k.WAV"
flnm="/home/igor/Downloads/googlebooks-eng-all-1gram-20120701-u"
flnm="/home/igor/Downloads/googlebooks-eng-all-1gram-20120701-m"

#===============================================================================
# thr_count_bytes(b'aa',flnm)
# sin_count_bytes(b'aa',flnm)
# singen_count_bytes(b'aa',flnm)
#===============================================================================

#%timeit thr_count_bytes(b'aa',flnm)
%time thr_count_bytes(b'aa',flnm)

#%timeit thr_count_bytes(b'aa',flnm,5)
%time thr_count_bytes(b'aa',flnm,5)

#%timeit thr_count_bytes(b'aa',flnm,20)
%time thr_count_bytes(b'aa',flnm,20)

#%timeit sin_count_bytes(b'aa',flnm)
%time sin_count_bytes(b'aa',flnm)

%time singen_count_bytes(b'aa',flnm)


