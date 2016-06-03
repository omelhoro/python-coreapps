#!/usr/bin/env python

'''
Created on Jun 21, 2014

@author: igor
'''
from time import ctime
from cgi import escape

i=0
hist=[]
formattoP=lambda x: "<p>%s</p>" %x

def application(env,start_response):
   #i+=1
   hist.append(ctime())
   status = '200 OK'
   headers = [('Content-type', 'text/html')]
   start_response(status,headers)
   return map(formattoP,hist)
   #return ["".join(map(formattoP,hist))]
   #return [escape(env.get('CONTENT_LENGTH', 0))]
   #return [str(env)]

#if __name__ == '__main__':
#    application(env,start_response)