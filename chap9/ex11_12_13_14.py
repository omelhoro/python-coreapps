'''
Created on Jun 4, 2014

@author: igor
'''
'''
Created on Jun 2, 2014

@author: igor
'''
#!/usr/bin/env python

import cStringIO
import formatter
from htmllib import HTMLParser
import httplib
import os
import sys
import urllib
import urlparse

urllib.FancyURLopener


class My404UrlOpener(urllib.FancyURLopener):
    
    def http_error_404(self, url, fp, errcode, errmsg, headers, data=None):
        'Handles 404 error with retrying to add slash and open again'
        if not url.endswith("/"):
            self.open(url+"/")


class LinkImageParser(HTMLParser):
    
    def __init__(self, formatter, verbose=0):
        HTMLParser.__init__(self,formatter, verbose)
        self.imagelist=[]
    
    def handle_image(self,src, alt, *args):
        print("-"*10+src)
        self.imagelist.append(src)
        

urllib._urlopener=My404UrlOpener()        

class Retriever(object):
    __slots__ = ('url', 'file')
    def __init__(self, url):
        self.url, self.file = self.get_file(url)

    def get_file(self, url, default='index.html'):
        'Create usable local filename from URL'
        parsed = urlparse.urlparse(url)
        host = parsed.netloc.split('@')[-1].split(':')[0]
        filepath = '%s%s' % (host, parsed.path)
        if not os.path.splitext(parsed.path)[1]:
            filepath = os.path.join(filepath, default)
        linkdir = os.path.dirname(filepath)
        if not os.path.isdir(linkdir):
            if os.path.exists(linkdir):
                os.unlink(linkdir)
            os.makedirs(linkdir)
        return url, filepath

    def download(self):
        'Download URL to specific named file'
        try:
            retval = urllib.urlretrieve(self.url, self.file)
        except (IOError, httplib.InvalidURL) as e:
            retval = (('*** ERROR: bad URL "%s": %s' % (
                self.url, e)),)
        return retval

    def parse_links(self,parser):
        'Parse out the links found in downloaded HTML file'
        with open(self.file, 'r') as f:
            data = f.read()
        return parser(data,self.file)


class Crawler(object):
    count = 0

    def __init__(self, url,parser):
        self.parser=parser
        self.q = [url]
        self.seen = set()
        parsed = urlparse.urlparse(url)
        host = parsed.netloc.split('@')[-1].split(':')[0]
        self.dom = '.'.join(host.split('.')[-2:])

    def get_page(self, url, media=False):
        'Download page & parse links, add to queue if nec'
        r = Retriever(url)
        fname = r.download()[0]
        if fname[0] == '*':
            print fname, '... skipping parse'
            return
        Crawler.count += 1; 
        print("\n{0}\nURL: {1}\nFILE: {2}".format(Crawler.count,url,fname))
        self.seen.add(url)
        ftype = os.path.splitext(fname)[1]
        if ftype not in ('.htm', '.html'):
            return

        for link in r.parse_links(self.parser):
            if link.startswith(('mailto:',"telnet:","news:","gopher:","about:")):
                print '... discarded, mail/misc link'
                continue
            if not media:
                ftype = os.path.splitext(link)[1]
                if ftype in ('.mp3', '.mp4', '.m4v', '.wav'):
                    print '... discarded, media file'
                    continue
            if not link.startswith(('http://',"ftp://")):
                link = urlparse.urljoin(url, link)
            print '*', link,
            if link not in self.seen:
                if self.dom not in link:
                    print '... discarded, not in domain'
                else:
                    if link not in self.q:
                        self.q.append(link);print '... new, added to Q'
                    else:
                        print '... discarded, already in Q'
            else:
                    print '... discarded, already processed'

    def go(self, media=False):
        'Process next page in queue (if any)'
        #while self.q :
        while Crawler.count < 10 and self.q  :
            url = self.q.pop()
            self.get_page(url, media)


def parsersetup():
    def fbeatifulsoup():
        from BeautifulSoup import BeautifulSoup as bs
        from BeautifulSoup import SoupStrainer
        
        def try_attrib(e,attrib="href"):
            try:
                return e[attrib]
            except KeyError:
                return "Nolinkinside"
        
        def parse(data,fl):
            filtdata=(try_attrib(x,'href') for x in bs(data, parseOnlyThese=SoupStrainer('a')))
            return filtdata
        return parse
        
    def fhtml5lib():
        from html5lib import parse as parse5, treebuilders
        
        def try_attrib(e,attrib):
            
            try:
                a=e.attributes["href"]
                print(e.attributes["href"])
                return a
            except:
                pass
        
        def parse(data,fl):
            filtdata=(try_attrib(e, "href") for e in parse5(data))
            return (e for e in filtdata if e)
        return parse
        

    def flxml():
        import lxml.etree as et
        parser=et.HTMLParser()

        def parse(data,fl):
            filtdata=(find.attrib["href"] for find in et.parse(fl,parser).iter("a"))
            return filtdata
        return parse

    def fhtmlp():
        #parser = HTMLParser(formatter.AbstractFormatter(formatter.DumbWriter(cStringIO.StringIO())))
        parser = LinkImageParser(formatter.AbstractFormatter(formatter.DumbWriter(cStringIO.StringIO())))

        def parse(data,fl):
            parser.feed(data)
            parser.close()
            return parser.anchorlist
        return parse
    
    choices=[(fbeatifulsoup,"BeatifulSoup"),(fhtml5lib,"html5lib"),(flxml,"lxml"),(fhtmlp,"HtmlParser")]
    formatted="".join(["{0}. {1}\n".format(i+1,nm) for i,(_,nm) in enumerate(choices)])
    choice=int(raw_input(formatted))
    if choice in range(1,5):
        return choices[choice-1][0]()
    else:
        print("Invalid choice. Choose again:")
        parsersetup()
        
    

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url= "http://127.0.0.1/wordpress/projects/"
        #url= "ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/0.8/"
        #url= "www.prenhallprofessional.com "
        #=================================================================================
        # try:
        #     url = raw_input('Enter starting URL: ')
        # except (KeyboardInterrupt, EOFError):
        #     url = ''
        #=================================================================================
    if not url:
        return
    if not url.startswith('http://') and \
        not url.startswith('ftp://'):
            url = 'http://%s/' % url.strip()
    
    parser=parsersetup()
    robot = Crawler(url,parser)
    robot.go()

if __name__ == '__main__':
    main()