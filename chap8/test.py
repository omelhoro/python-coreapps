'''
Created on Jun 2, 2014

@author: igor
'''

import ctypes
import os

os.chdir("/home/igor/workspace_scala/Book-Python-Coreapps/chap8/")
o=ctypes.CDLL("Extest.so")

def fac(i):
    if i==1:
        return 1
    else:
        return i*fac(i-1)
    
def factail(i):
    def loop(i,cur):
        if i==1:
            return 1
        else:
            return loop(i-1,cur*i)
    return loop(i,1)

%timeit fac(10)
%timeit factail(10)
%timeit o.fac(10)
%timeit reduce(lambda a,b: a*b,xrange(10,1,-1))
%timeit reduce(lambda a,b: a*b,xrange(1,10))
%timeit reduce(lambda a,b: a*b,range(1,10))

c=ctypes.c_char_p("Igor")
o.reverse.restype=ctypes.c_char_p

%timeit Extest.doppel("Igor")
%timeit o.reverse("Igor")
%timeit "Igor"[::-1]

