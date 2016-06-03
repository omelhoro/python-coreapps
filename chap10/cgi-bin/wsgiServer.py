#!/usr/bin/env python
'''
Created on Jun 21, 2014

@author: igor
'''

from wsgiref.simple_server import make_server
#import wsgiApp as wa
import ex19 as wa

PORT=8000

httpd = make_server('', PORT, wa.application)
print "Started app serving on port %s..." %PORT
httpd.serve_forever()

