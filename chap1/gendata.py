'''
Created on Apr 9, 2014

@author: igor
'''
from random import randrange, choice
from string import ascii_lowercase as lc
from sys import maxint
from time import ctime

tlds = ('com', 'edu', 'net', 'org', 'gov')

def make_randstr(n):
    def gen_str():
        dtint = randrange(maxint)     # pick date
        dtstr = ctime(dtint)          # date string
        llen = randrange(4, 8)        # login is shorter
        login = ''.join(choice(lc) for _ in range(llen))
        dlen = randrange(llen, 13)   # domain is longer
        dom = ''.join(choice(lc) for _ in xrange(dlen))
        return  '%s::%s@%s.%s::%d-%d-%d' % (dtstr, login,
            dom, choice(tlds), dtint, llen, dlen)
    if not n:
        return []#gen_str()
    else:
        s=gen_str()
        return  [s]+make_randstr(n-1)

def make_randstr_1(n):
    for _ in xrange(n):
        dtint = randrange(maxint)     # pick date
        dtstr = ctime(dtint)          # date string
        llen = randrange(4, 8)        # login is shorter
        login = ''.join(choice(lc) for _ in range(llen))
        dlen = randrange(llen, 13)   # domain is longer
        dom = ''.join(choice(lc) for _ in xrange(dlen))
        yield '%s::%s@%s.%s::%d-%d-%d' % (dtstr, login,
            dom, choice(tlds), dtint, llen, dlen)


def main():
    l=make_randstr(6)
    with open("redata.txt","w+") as f:
        def writelines(l):
            if len(l)!=1:
                writelines(l[1:])
                f.writelines(l[0]+"\n")
            else:
                f.writelines(l[0]+"\n")
        writelines(l)

if __name__ == '__main__':
    main()