'''
Created on Jun 7, 2014

@author: igor
'''
#!/usr/bin/env python

import lxml.etree as et
from html5lib import parse, treebuilders
from BeautifulSoup import BeautifulSoup, SoupStrainer
from cStringIO import StringIO
from HTMLParser import HTMLParser
#from timeit import timeit
import timeit
from guppy import hpy
h = hpy()

with open("sport1.de/index.html") as f:
    source=f.read()

lst=[]

def source_read():
    with open("sport1.de/index.html") as f:
        source=f.read()
    return source

def try_attr_dct(e,attr):
    try:
        return getattr(e,"attrib")[attr] #lxml format
    except (TypeError,AttributeError):
        try:
            return getattr(e,"attributes")[attr] #html5lib format
        except (TypeError,AttributeError,KeyError):
            try:
                return e[attr] # BS format
            except (KeyError,TypeError):
                return None


def simpleBS(url, f):
    'simpleBS() - use BeautifulSoup to parse all tags to get anchors'
    
    parsed=BeautifulSoup(f)
    tags=parsed.findAll('a')
    data=(try_attr_dct(x, 'href')  for x in tags )
    #data=(x['href']  for x in tags )
    #print h.heap()
    return output(data)

def fasterBS(url, f):
    'fasterBS() - use BeautifulSoup to parse only anchor tags'
    parsed=BeautifulSoup(f, parseOnlyThese=SoupStrainer('a'))
    data=(try_attr_dct(x, "href") for x in parsed )
    #data=(x['href']  for x in parsed )
    #print h.heap()
    return output(data)

def htmlparser(url, f):
    'htmlparser() - use HTMLParser to parse anchor tags'
    
    class AnchorParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag != 'a':
                return
            if not hasattr(self, 'data'):
                self.data = []
            self.data.extend([v for k,v in attrs if k=="href"])
            #=============================================================================
            # for attr in attrs:
            #     if attr[0] == 'href':
            #         self.data.append(attr[1])
            #=============================================================================
                    
    parser = AnchorParser()
    parser.feed(f)
    data=(x for x in parser.data)
    #print(parser.data)
    return output(data)

def html5libparse(url, f):
    'html5libparse() - use html5lib to parse anchor tags'
    #parsed=filter(lambda x:isinstance(x, treebuilders.simpletree.Element) and x.name=="a" , parse(f))
    data=(try_attr_dct(x, "href") for x in parse(f))
    #data=(try_attr_dct(x, "href") for x in parsed)
    #data=(x.attributes["href"] for x in parsed)
    #print h.heap()
    return output(data)


def lxmlparsewrap(f):
    
    ff=StringIO(f)
    ff.seek(0)

    def lxmlparse(url,f):
        'parser built on lxml'
        ff=StringIO(f)
        ff.seek(0)
        parser=et.HTMLParser()
        tree=et.parse(ff,parser)
        data=(try_attr_dct(x, "href") for x in tree.iter("a"))
        return output(data)
    return lxmlparse

def lxmlparse(url,f):
    'parser built on lxml'
    ff=StringIO(f)
    ff.seek(0)
    parser=et.HTMLParser()
    tree=et.parse(ff,parser)
    data=(try_attr_dct(x, "href") for x in tree.iter("a"))
    #data=(x.attrib["href"] for x in tree.iter("a"))
    #print h.heap()
    return output(data)

def output(data):
    return data
    #joined="\n".join(data)
    #lst.append(joined)

flst=(simpleBS,fasterBS,htmlparser,html5libparse,lxmlparse)
print map(lambda x: len(filter(None,x)),(f("sport1.de",source) for f in flst))


timeit_str=lambda nm: ("{}('sport1.de',source)".format(nm),
                       "from __main__ import {},source_read; source=source_read()".format(nm))
for fn in flst:
    print fn
    s=timeit_str(fn.__name__)
    print timeit.timeit(*s,number=2)

#map(lambda fn=fn__name__: timeit(*timeit_str(get_fname(fn)) ,number=4)   ,flst)

#print timeit("fasterBS('sport1.de',source)","from __main__ import fasterBS,source_read; source=source_read()",number=4)

