'''
Created on Jun 3, 2014

@author: igor
'''


#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open("log.log","w+") as f:
            f.write(self.path)
        if self.path=="/image/":
            fl,flmime="casetr.png","image/png"
        elif self.path=="/text/":
            fl,flmime="test.txt","text/plain"
        elif self.path=="/":
            fl,flmime="index.html","text/html"
        else:
            self.send_error(404,'File Not Found: %s' % self.path)
            fl=""
        if fl:
            try:
                f = open(fl, 'rb')
                self.send_response(200)
                self.send_header('Content-type', flmime)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)

def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print 'Welcome to the machine...',
        print 'Press ^C once or twice to quit.'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()