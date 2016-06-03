# encoding: utf-8
'''
Created on Apr 7, 2014

@author: igor
'''
from re import findall,sub,search,match, split
#ex1
s="bat, bit, but, hat, hit, hut."
findall("\w{3}",s)

#ex2
s="Igor Fischer"
match("\w+\s\w+",s).group(0)

#ex3
s="Fischer, I. adsda"
match("\w+, \w",s).group(0)

#ex4??
match("[a-zA-Z_]",s)

#ex5
s="Kirschenweg 38 G"
match("(\w+)\s(\d+)\s(\w)",s).groups()

#ex6
s="www.google.com, www.yahoo.de, www.ucla.edu,www.faz.net"
findall("(www\.\w+\.(com|de|net|edu))",s)

#ex7
s="123456789"
match("(\d+)",s).groups()

#ex8
s="2L"
match("\d+L",s).group(0)

#ex9
s="2.345345"
match("\d+\.\d*",s).group(0)

#ex10??
s="-2.34435345"
match("[-]\d+\.\d+",s).group(0)

#ex11
s="fsdf sdfs igor.fischer-best154@studium.uni-hamburg.de "
findall(r"\s[A-Za-z0-9._-]+@[-A-Za-z0-9._]+",s)

#ex12
s="http://www.example.com/path/to/name "
findall("(http://)?(www\.)?(\w+)(\.com)",s)
findall("((http://)|(www\.).+?\s)",s)

#ex13
s=str(map(lambda x: str(type(x)),[0,'a',"asdf"]))
findall("\<type '(\w+)'\>",s)

#ex14
s="09 12 11 9,3,04,10,19"
findall("(1[0-2])|(0?[1-9][^1-9])",s)

#ex15
s="1234-123456-12345 123412345612345 1234-1234-1234-1234 1234123412341234"
#findall("\d{4}-\d{4,6}-\d{4,5} (?<=\d{4}-\d{4})-\d{4}?",s)
findall("(?:\d{4}-?\d{6}-?\d{5})|(?:\d{4}-?\d{4}-?\d{4}-?\d{4})",s)
rx="(?:\d{4}-?\d{6}-?\d{5})|(?:\d{4}-?\d{4}-?\d{4}-?\d{4})"
def check_cc(cc):
    toint=lambda x: map(int,str(x))
    cc_int=toint(str(cc).replace("-","")) 
    cc_newint=[]
    for i,n in enumerate(cc_int[-2::-1]):
        if i%2==0:
            dn=n*2
            if dn>10:
                cc_newint.append(sum(toint(dn)))
            else:
                cc_newint.append(dn)
        else:
            cc_newint.append(n)
            
    cc_sum=sum(cc_newint)
    return cc_sum

def find_cc(s,rx):
    for cc in findall(rx,s):
        yield check_cc(cc)

isvalid=lambda x: x%10==0
#for sm in find_cc(s, rx):
#    print(isvalid(sm),sm)

cc_nums=[ 79927398710, 79927398711, 79927398712, 79927398713, 79927398714, 79927398715, 79927398716, 79927398717, 79927398718, 79927398719] 
for cc_num in cc_nums[:2]:
    cc_sum=check_cc(cc_num)
    print(cc_sum,isvalid(cc_sum))

#ex17
#from gendata import main
import os
from collections import Counter
s="""
Tue May 24 06:01:38 2033::lhtriqp@bsunglmkb.com::2000520098-7-9
Thu Jun  1 22:11:02 1978::cawi@ogloz.net::265583462-4-5
Sat Aug 14 09:41:19 1993::ftpcig@scwecwlilqr.net::745314079-6-11
Wed Jul 11 16:27:00 2001::myhmy@xuamxqogpy.com::994861620-5-10
Wed Apr 13 08:24:38 2005::zvathg@nlwfplnfavm.com::1113373478-6-11
Thu Aug  8 23:36:57 1974::ilgzmi@okbyvsvycqlc.com::145233417-6-12"""

pth="/home/igor/workspace_scala/Book-Python-Coreapps/"
os.chdir(pth)

def count_days():
    with open("redata.txt") as f:
        return findall("(?<! )\w{3} ",f.read())

def make_redate(n):
    os.system("python gendata.py")
    l=count_days()
    if n:
        return l+make_redate(n-1)
    else:
        return l
        
#Counter(make_redate(150))

#ex18
import time as t
dt=findall("(?P<tstring>\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}).+?::(?P<tint>[0-9]+)-",s)

def checktime_r(l):
    def check(tpl):
        tstring,tint=tpl
        ismatch=tstring==t.ctime(int(tint))
        return ismatch
    if l:
        return [check(l[0])]+checktime_r(l[1:])
    else:
        return []

checktime_r(dt)

#ex19
findall("(?P<tstring>\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4})",s)

#ex20
findall(r"(?P<email>\w+@\w+\.\w{3})",s)

#ex21
findall("\w{3} (?P<month>\w{3}) \d{1,2} \d{2}:\d{2}:\d{2} \d{4}",s)

#ex22
findall("\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} (?P<year>\d{4})",s)
        
#ex23
findall("\w{3} \w{3} \d{1,2} (?P<time>\d{2}:\d{2}:\d{2}) \d{4}",s)
        
#ex24
findall(r"(?P<login>\w+@\w+)\.\w{3}",s)

#ex25
findall(r"(?P<login>\w+)@(?P<domain>\w+)\.\w{3}",s)

#ex26
sub(r"(?P<email>\w+@\w+\.\w{3})","igor.fischer154@gmail.com",s)

#ex27
def format_time_r(l):
    def format_dt(m):
        md=m.groupdict()
        return "{m},{d},{y}".format(m=md["month"],d=md["day"],y=md["year"])
    if l:
        mobj=search("\w{3} (?P<month>\w{3}) {1,2}(?P<day>\d{1,2}) [0-9:]+ (?P<year>\d{4})",l[0])
        print(l[0],mobj)
        return [format_dt(mobj)]+format_time_r(l[1:])
    else:
        return []
        
format_time_r(split("\n",s)[1:-1])

#ex28
s="""
800-555-1212 
555-1212
(800) 555-1212
"""
findall(r"(?:\d{3}-)?\d{3}-\d{4}",s)

#ex29
findall(r"(?:\(?\d{3}\)?[- ]?)?\d{3}-\d{4}",s)
