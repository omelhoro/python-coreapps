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
import cPickle

LOGIN="""
<html>
<head><title>Login form</title></head>
<body>
%s
<form>
Username <input type="text"name='usern' value="if154" ><br>
Password <input type="password" name='passw' value="stalker" ><br>
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


mask=lambda up:map(lambda x: unichr(ord(x)+SHIFT) ,unicode(up))
#cPickle.dump({k:"".join(mask(itm)) for k,itm in example_logins.viewitems()},open("data/passw.dat","wb+"))

def set_cookie():
    cookie_string = os.environ.get('HTTP_COOKIE')
    if not cookie_string:
        c=Cookie.SimpleCookie()
        c["lastlogin"]=str(time())+str(ctime())
        c["lastlogin"]['max-age'] = 20
        print c

def get_cookie():
    cookie_string = os.environ.get('HTTP_COOKIE')
    return bool(cookie_string)
     

def check_pass(usern,upass):
    with open("cgi-bin/data/passw.dat") as f:
        passdb=cPickle.load(f)
    try:
        rpassw=passdb[usern]
        up=map(lambda x: unichr(ord(x)+SHIFT) ,unicode(upass))
        if "".join(up)==rpassw:
            set_cookie()
            return True
        else:
            return False
    except KeyError:
        return False
    
def login():
    form=cgi.FieldStorage()
    if get_cookie():
        return True
    try:
        usern,upass=form["usern"].value,form["passw"].value
        check_pass(usern, upass)
    except KeyError:
        #pass
        print(LOGIN)
        #return False

def render_form(warning=""):
    print(LOGIN %(warning))

if __name__ == '__main__':
    import cgitb; cgitb.enable(display=True)
    login()