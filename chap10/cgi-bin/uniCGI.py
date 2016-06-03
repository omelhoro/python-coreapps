#!/usr/bin/env python3
#encoding=utf8
'''
Created on Jun 21, 2014

@author: igor
'''

CODEC = 'UTF-8'
UNICODE_HELLO = u'''
Hello!
\u00A1Hola!
\u4F60\u597D!
\u3053\u3093\u306B\u3061\u306F!
Привет всем!
'''

import os
os.getenv("PYTHONIOENCODING")
os.environ["PYTHONIOENCODING"]
sys.getfilesystemencoding()

print('Content-Type: text/html; charset=%s\r'% CODEC) 
print('\r')
print('<HTML><HEAD><TITLE>Unicode CGI Demo</TITLE></HEAD>')
print('<BODY>')
#print(UNICODE_HELLO.encode(CODEC))
print(UNICODE_HELLO)
print('</BODY></HTML>')