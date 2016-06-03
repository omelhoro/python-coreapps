'''
Created on May 5, 2014

@author: igor
'''
import os
from MyThread import MyThread as Thread
import re
path="/home/igor/tmp/email_python/"
RE=r"(?:[a-zA-Z1-9]+@[a-zA-Z]\.[a-z]{1,3})|(?:www\.[a-zA-Z0-9]+\.[a-z]{1,3}) "
RE=r"www\.[a-zA-Z0-9-.]+\.[a-z]{1,3}(?=[ )])"
RE=r"(?:[a-zA-Z1-9.]+@[a-zA-Z-.]+\.[a-z]{1,3}) |(?:www\.[a-zA-Z0-9-.]+\.[a-z]{1,3}(?=[ )]))"

def make_links_glob(path,RE,n_bins=10,n_subset="all"):
    
    def make_links(fls):
        comp_txt=[]
        for fl in fls:
            with open(path+fl) as f:
                comp_txt.append(RE.sub(lambda x: r"<a href='http://{}'>Link</a>".format(x.group(0)),f.read()))
        
        return "".join(comp_txt)
    
    fls=os.listdir(path)
    
    if n_subset!="all" and isinstance(n_subset,tuple):
        fls=fls[n_subset[0]:n_subset[1]]
    bins=[ fls[r:r+len(fls)/n_bins] for i,r  in enumerate(range(0,len(fls),len(fls)/n_bins)) if i!=n_bins]
    RE=re.compile(RE)
    threads=[Thread(make_links,(b,)) for b in bins]
    [thr.start() for thr in threads ]
    [thr.join() for thr in threads ]
    #===========================================================================
    # with open("/home/igor/tmp/comp_mail.html","w") as f:
    #     f.write("".join([thr.getResult() for thr in threads ]))
    #===========================================================================


%time make_links_glob(path, RE,30,)
%time make_links_glob(path, RE,20,)
%time make_links_glob(path, RE,10,)
%time make_links_glob(path, RE,5,)


RE=r"(?:[a-zA-Z1-9.]+@[a-zA-Z-.]+\.[a-z]{1,3}) |(?:www\.[a-zA-Z0-9-.]+\.[a-z]{1,3}(?=[ )]))"
foo="Forscser.giro@studoim.hamburg-ino.de (www.klimacampus.de) www.cen.uni-hamburg.de "

re.sub(RE,lambda x: r"<a href='{}'>Link</a>".format(x.group(0)),foo)
