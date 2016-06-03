#!/usr/bin/env python
#encoding=utf8
'''
Created on Jun 15, 2014

@author: igor
'''
import cgi
import Cookie
from time import ctime, time
import os
import sys

LOGIN="""
<html>
<head><title>Login form</title></head>
<body>
%s
<form>
Username <input type="text"name='usern' ><br>
Password <input type="password" name='passw'><br>
<input type="submit"><br>
</form>
</body>
</html>"""

SECRET="""
<html>
<head><title>Main Site</title></head>
<body>
Now you can see the secret!
</body>
</html>"""

reload(sys)
sys.setdefaultencoding("utf8")



SHIFT=99
example_logins={
                "igor":u"хаха",
                "ig154":u"käse",
                "if154":"stalker"
                }

def add_credens(un,up):
    np=map(lambda x: unichr(ord(x)+SHIFT) ,unicode(up))
    print("".join(np))
    with open("passws.txt","a") as f:
        f.write(u"{un},{up}\n".format(un=un,up="".join(np)))

#[add_credens(un, up) for un,up in example_logins.viewitems()]

def set_cookie():
    cookie_string = os.environ.get('HTTP_COOKIE')
    if not cookie_string:
        c=Cookie.SimpleCookie()
        c["lastlogin"]=str(time())+str(ctime())
        c["lastlogin"]['max-age'] = 15
        print c

def get_cookie():
    cookie_string = os.environ.get('HTTP_COOKIE')
    return bool(cookie_string)
     

def check_pass(usern,upass):
    with open("cgi-bin/pasws.txt") as f:
        passws=dict(map(lambda x: x.strip().split(",") ,f.readlines()))
    try:
        rpassw=passws[usern]
        up=map(lambda x: unichr(ord(x)+SHIFT) ,unicode(upass))
        if "".join(up)==rpassw:
            set_cookie()
            print(SECRET)
        else:
            render_form("Password not correct!")
    except KeyError:
        render_form("No such username. %s" %passws[usern])
    
def login():
    form=cgi.FieldStorage()
    try:
        usern,upass=form["usern"].value,form["passw"].value
        check_pass(usern, upass)
    except KeyError:
        render_form("Credentials not complete")

def render_form(warning=""):
    print(LOGIN %(warning))

if __name__ == '__main__':
    import cgitb; cgitb.enable(display=True)
    if get_cookie():
        print SECRET
    else:
        login()
