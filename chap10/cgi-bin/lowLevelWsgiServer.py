'''
Created on Jun 21, 2014

@author: igor
'''
import sys
import ex19
import os

#=========================================================================================
# def run_wsgi_app(app, environ):
#     body = StringIO.StringIO()
# 
#     def start_response(status, headers,exc_info=None):
#         if exc_info is None:
#             body.write('Status: %s\r\n' % status)
#             for header in headers:
#                 body.write('%s: %s\r\n' % header)
#             return body.write
# 
#     iterable = app(environ, start_response)
#     try:
#       if not body.getvalue():
#             raise RuntimeError("start_response() not called by app!")
#       body.write('\r\n%s\r\n' % '\r\n'.join(line for line in iterable))
#     finally:
#         if hasattr(iterable, 'close') and callable(iterable.close):
#             iterable.close()
# 
#     sys.stdout.write(body.getvalue())
#     sys.stdout.flush()
#     
#     
# run_wsgi_app(ex19.application, os.environ) 
#=========================================================================================

def run_wsgi_app(app, environ):
    body = []

    written=False
    def start_response(status, headers,exc_info=None):
        if exc_info is None:
            body.append(("status",'Status: %s\r\n' % status))
            for header in headers:
                body.append(("header",'%s: %s\r\n' % header))
            return body
        else:
            if not written:
                [body.pop(i) for i,itm in enumerate(body) if itm[0]=="header"]
                body[0]=("status",status)
                for hd in headers[::-1]:
                    body.insert(1,("header",hd))
            else:
                raise exc_info[1]

    iterable = app(environ, start_response)
    try:
      if not body:
            raise RuntimeError("start_response() not called by app!")
      body.append(("body",'\r\n%s\r\n' % '\r\n'.join(line for line in iterable)))
    finally:
        if hasattr(iterable, 'close') and callable(iterable.close):
            iterable.close()

    sys.stdout.write("".join(list(zip(*body))[1]))
    sys.stdout.flush()
    written=True
    
    
run_wsgi_app(ex19.application, os.environ) 
