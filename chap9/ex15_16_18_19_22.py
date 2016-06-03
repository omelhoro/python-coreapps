'''
Created on Jun 7, 2014

@author: igor
'''
#!/usr/bin/env python

from HTMLParser import HTMLParser
from cStringIO import StringIO
from urllib2 import urlopen
from urlparse import urljoin
import inspect
from BeautifulSoup import BeautifulSoup, SoupStrainer
from html5lib import parse, treebuilders
from distutils.log import warn
import sys
from _functools import partial
import lxml.etree as et
from lxml.etree import HTMLParser as LXMLParserHtml
from random import randint
from sys import stdout
import os
import subprocess as sb
import re
URLs = (
    'http://python.org',
    'http://google.com',
)

def simpleBS(url, f):
    'simpleBS() - use BeautifulSoup to parse all tags to get anchors'
    parsed=BeautifulSoup(f)
    tags=parsed.findAll('a')
    data=(urljoin(url, x['href']) for x in tags )
    output(data)

def fasterBS(url, f):
    'fasterBS() - use BeautifulSoup to parse only anchor tags'
    parsed=BeautifulSoup(f, parseOnlyThese=SoupStrainer('a'))
    data=(urljoin(url, x['href']) for x in parsed )
    output(data)

def htmlparser(url, f):
    'htmlparser() - use HTMLParser to parse anchor tags'
    class AnchorParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag != 'a':
                return
            if not hasattr(self, 'data'):
                self.data = []
            for attr in attrs:
                if attr[0] == 'href':
                    self.data.append(attr[1])
    parser = AnchorParser()
    parser.feed(f.read())
    output(urljoin(url, x) for x in parser.data)

def html5libparse(url, f):
    'html5libparse() - use html5lib to parse anchor tags'
    parsed=filter(lambda x:isinstance(x, treebuilders.simpletree.Element) and x.name=="a" , parse(f))
    data=(urljoin(url, x.attributes['href']) for x in parsed)
    output(data)

def lxmlparse(url,f):
    parser=LXMLParserHtml()
    tree=et.parse(f,parser)
    data=((urljoin(url,itm.attrib["href"]) for itm in tree.iter("a")))
    output(data)
    
    
def process(url, data):
    print '\n*** simple BS'
    simpleBS(url, data)
    data.seek(0)
    print '\n*** faster BS'
    fasterBS(url, data)
    data.seek(0)
    print '\n*** HTMLParser'
    htmlparser(url, data)
    data.seek(0)
    print '\n*** HTML5lib'
    html5libparse(url, data)
    data.seek(0)
    print '\n*** Lxml'
    lxmlparse(url, data)

def main(args):
    for url in URLs:
        f = urlopen(url)
        data = StringIO(f.read())
        f.close()
        process(url, data)

def choose_verbosity():
    
    def write_file(data):
        rand_name=lambda: "".join(chr(randint(97,122)) for _ in range(7))+".log"
        with open(rand_name(),"w+") as f:
            f.write(data)
    
    def write_stdin(data):
        stdout.write(data)
    
    def write_process(data):
        proc=sb.Popen("./a.out",stdin=sb.PIPE,stdout=sb.PIPE)
        proc.stdin.write(data)
        proc.stdin.close()
        res=proc.stdout.read()

        print res
        proc.wait()
    
    def sort_wwws(link):
        return re.sub("https?://(www\.)?","",link)
    
    def output(x, verbs="all",f=write_stdin):
        if verbs=="all":
            print '\n'.join(sorted(set(x)))
            return None
        else:
            cframe = inspect.currentframe()
            func = inspect.getframeinfo(cframe.f_back).function
            print 'called from ' + func
            if verbs==func:
                data='\n'.join(sorted(set(x),key=sort_wwws))
                f(data)

    choices=("simpleBS","fasterBS","htmlparser","html5libparse","lxmlparse","all")
    intro="\n".join( "{0}. {1}".format(i+1,nm) for i,nm in enumerate(choices))+"\n>"
    choice=raw_input(intro)
    try:
        ichoice=int(choice)-1
        try:
            return partial(output, verbs=choices[ichoice],f=write_stdin)
        except IndexError:
            warn("Not a valid choice. Try again:")
            return choose_verbosity()
    except:
        warn("Not a valid integer. Try again:")
        return choose_verbosity()
    
    
        
        
if __name__ == '__main__':
    output=choose_verbosity()
    main(sys.argv)

links="""http://google.com/advanced_search?hl=de&authuser=0
http://google.com/intl/de/about.html
http://google.com/intl/de/ads/
http://google.com/intl/de/policies/
http://google.com/language_tools?hl=de&authuser=0
http://google.com/preferences?hl=de
http://google.com/services/
http://maps.google.de/maps?hl=de&tab=wl
http://news.google.de/nwshp?hl=de&tab=wn
http://www.google.de/history/optout?hl=de
http://www.google.de/imghp?hl=de&tab=wi
http://www.google.de/intl/de/options/
http://www.google.de/setprefdomain?prefdom=US&sig=0_KH00sYgX2vuW5PMZyQOoxlr3iiA%3D
http://www.youtube.com/?gl=DE&tab=w1
https://accounts.google.com/ServiceLogin?hl=de&continue=http://www.google.de/%3Fgfe_rd%3Dcr%26ei%3DZFeTU5rUHYGm8wekvIHIDQ
https://drive.google.com/?tab=wo
https://mail.google.com/mail/?tab=wm
https://play.google.com/?hl=de&tab=w8
https://plus.google.com/117570067846637741468"""

foo="""http://python.org/psf/
http://python.org/search
http://roundup.sourceforge.net/
http://sourceforge.net/projects/mysql-python
https://twistedmatrix.com/trac/
http://wiki.python.org/moin/
http://wiki.python.org/moin/CgiScripts
https://www.python.org/
www.python.org"""
import re
sub_prot=lambda link:re.sub("https?://(www\.)?",lambda x: "[{0}]".format(x.group(0)),link)
map(sub_prot, links.split("\n"))



