'''
Created on May 5, 2014

@author: igor
'''
import os
from MyThread import MyThread as Thread
import re
import cProfile as cp



def replace_links(flnm,n_threads=10):

    def replace(flnm="/home/igor/bin/praat-old",start=0,step=1024,i=1):
        print("start {}".format(i))
        with open(flnm,"rb") as f:
            f.seek(start)
            txt=f.read(step)
            print(len(txt),start,step,txt[:5],i)
            res=rec.sub(lambda x: r"<a href='http://{}'>Link</a>".format(x.group(0)),txt)
            print("done {}".format(i))
            return res
    
    rec=re.compile(RE)
    step=os.path.getsize(flnm)/n_threads
    flnm_size=range(0,os.path.getsize(flnm),step)
    threads=[Thread(replace,args=(flnm, i, step,j)) for j,i in enumerate(flnm_size)]
    print(len(threads))
    [th.start() for th in threads]
    [th.join() for th in threads]
    b="".join([th.getResult() for th in threads])

RE=r"(?:[a-zA-Z1-9.]+@[a-zA-Z-.]+\.[a-z]{1,3}) |(?:www\.[a-zA-Z0-9-.]+\.[a-z]{1,3}(?=[ )]))"
flnm="/home/igor/tmp/comp_mail.html"

#===============================================================================
# %time replace_links(flnm)
# %time replace_links(flnm,20)
# %time replace_links(flnm,30)
#===============================================================================


#print(cp.run("replace_links(flnm)", sort="cumulative"))
print(cp.run("replace_links(flnm,20)", sort="cumulative"))
