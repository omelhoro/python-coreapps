'''
Created on Jun 21, 2014

@author: igor
'''
import cgi
from cgi import parse_qs
from time import ctime

HTML="""
<html>
<head><title>Feedback</title></head>
<body>
<nav>
<a href='/showComms/'>Show all comments</a>
<a href='/'>Home</a>
<a href='/makeComms/'>Leave a comment</a>
</nav>
%s
</body>
</html>"""

FORMBODY= HTML % ('''
<form method=POST action='/postComms/' >
<p><label>Your email</label><input type=text name=email value=' '></p>
<p><label>Your comment</label><input type=text name=text size=60 value=' '></p>
<input type=submit>
</form>
''')

THANK='<p>Thank you</p>'
ERROR_EM="<p>Not a valid email!</p>"
ERROR_CO="<p>No comment!</p>"

db=[]

def post(environ,start_response):
    lenPost=environ.get('CONTENT_LENGTH', 0)
    request_body = environ['wsgi.input'].read(int(lenPost))
    d = parse_qs(request_body)
    em=d.get("email",[""])
    com=d.get("text",[""])
    db.append((em[0],ctime(),com[0]))
    return show(environ,start_response)

def show(environ,start_response):
    formatentry=lambda x: "<p><span>%s</span> said (%s) : %s</p>" %(x[0],x[1],x[2])
    entrys=map(formatentry,db)
    start_response()
    return [HTML % "".join(entrys) ]

def create_com(environ,start_response):
    start_response()
    return [FORMBODY]
    
def index(environ,start_response):
    start_response()
    return [HTML % "This is the worlds best site!"]

def application(environ,start_response):
    path=environ.get('PATH_INFO', 0)
    urls={"/":index,
    "/postComms/":post,
    "/makeComms/":create_com,
    "/showComms/":show}
    start_response_filled=lambda status='200 OK',headers=[('Content-type', 'text/html')]: start_response(status,headers)
    return urls.get(path,index)(environ,start_response_filled)
    
#if __name__ == '__main__':
#    process()