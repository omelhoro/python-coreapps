'''
Created on Jun 3, 2014

@author: igor
'''
from __main__ import sys
import urllib2 as u2
import urllib as u
import urlparse as up
from _functools import reduce



def main(args):
    
    def formatfname(flnm):
        slash=lambda x: x.replace("/","--")
        fns=[slash]
        return reduce(lambda a,fn: fn(a),fns,flnm) 
    
    if len(args) >1:
        url=args[1]
        d=u2.urlopen(url)
        with open(formatfname(url),"w+") as f:
            f.write(d.read()) 
    else:
        print("Not enough args.")

#main(('pass',"http://www.sport1.de"))
#main(('pass',"http://www.sport1.de/de/fussball/fus_international/newspage_901484.html"))
#main(('pass',"https://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/19.0-candidates/build1/KEY"))

import os
os.path.normpath("http://www.sport1.de")

if __name__ == '__main__':
    main(sys.argv)