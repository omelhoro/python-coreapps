'''
Created on Jun 3, 2014

@author: igor
'''
import lxml.etree as et


def column_links(bkms="bookmarkslinuxPort.html"):
    html=et.HTMLParser()
    tree=et.parse(bkms,html)
    caplen=lambda i,t: t[:80] if i > 80 else t
    for a in tree.iter("a"):
        t,l=a.text,a.attrib["href"]
        print(caplen(len(t),t).ljust(80),caplen(len(l),l).ljust(80))
    

column_links()

        
        
        
