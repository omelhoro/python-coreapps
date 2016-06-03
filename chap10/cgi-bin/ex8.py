#!/usr/bin/env python
# encoding=utf8
'''
Created on Jun 16, 2014

@author: igor
'''
import loginsys
import cgi
import cPickle
from loginsys import SHIFT
from random import randint
import os
import shelve
import pickle

format_url=lambda x: "/cgi-bin/ex8.py?action={}".format(x)

SCTT="""
<html>
<head><title>%s</title></head>
<body>
%s
</body>
</html>"""

LOGIN=SCTT % ("Login form","""
<form method=post action=%s>
Username <input type="text"name='usern' value="if154" ><br>
Password <input type="password" name='passw' value="stalker" ><br>
<input type="submit"><br>
</form>
""" %(format_url("login")) )

FIRSTPAGE=SCTT % ("Priv level","""
<a href=%s>Guest</a>
<a href=%s>Member</a>
""" % (format_url("guest"),format_url("member"))
)

SECRET=SCTT %("Guest privs","Now you can see the secret!")

TABLE=SCTT %("Logged privs","<table>%s</table>")

FAIL=SCTT %("Login failed","Wrong credens")

EDIT=SCTT %("Edit entry","""<form method=post action=%s >
    <input name='usern' value=%s >
    <input name='adress' value= %s>
    <input type=submit value='Submit changes'>""")

PATH="cgi-bin/data/"
FL="dbase.dat"

class UserEntry(object):
    
    def __init__(self,name,adress):
        self.name=name
        self.adress=adress

HEADERS=("name","adress")

def create_db():
    rand_nums=lambda n: "".join([str(randint(1,14)) for _ in range(n)])
    nms=("Igor","Johanna","Julian","Phillip","Julia")
    db=shelve.open(PATH+FL)
    db["persons"]=[UserEntry(nm, rand_nums(5)) for nm in nms]
    db.close()

try:
    os.listdir(PATH)
except OSError:
    PATH="data/"
    
if FL not in os.listdir(PATH):
    create_db()

def login():
    
    def check_pass(usern,upass):
        with open("cgi-bin/data/passw.dat") as f:
            passdb=cPickle.load(f)
        try:
            rpassw=passdb[usern]
            up=map(lambda x: unichr(ord(x)+SHIFT) ,unicode(upass))
            if "".join(up)==rpassw:
                loginsys.set_cookie()
                show_db(True)
            else:
                show_fail(passdb)
        except KeyError:
            print(LOGIN)
        
    form=cgi.FieldStorage()
    try:
        action=form["action"].value
    except KeyError:
        print(FIRSTPAGE)
        return None
    if action=="login":
        usern,upass=form["usern"].value,form["passw"].value
        check_pass(usern, upass)
    elif action== "guest":
        show_db(False)
    elif action=="member":
        if loginsys.get_cookie():
            show_db(True)
        else:
            print(LOGIN)
    elif action.startswith("edit"):
        edit(action[4:])
    elif action.startswith("upda"):
        update(action[4:],form)

def update(ky,form):
    un,ad=form["usern"].value,form["adress"].value
    db=access_db()
    p=filter(lambda x: x.name==ky,db["persons"])[0]
    p.name=un.replace(" ","_")
    p.adress=ad
    db.sync()
    db.close()
    show_db(True)

def edit(ky):
    db=access_db()
    p=filter(lambda x: x.name==ky,db["persons"])[0]
    print(EDIT %(format_url("upda"+p.name),p.name,p.adress))
    db.close()

def access_db():
    db=shelve.open(PATH+FL,writeback=True)
    return db

def show_db(ismember=False):
    
    def render_edit_butts(ky):
        if ismember:
            return "<a href=%s><button>Edit</button> </a>" % format_url("edit%s" % ky)
        else:
            return ""
    render_th=lambda x: "<th>%s</th>" %x
    render_td=lambda x: "<td>%s</td>" %x if x else ""
    render_tr=lambda *x: "<tr>%s</tr>" %"".join(*x)
    db=access_db()
    tabs=[render_tr(map(render_td,(_.name,_.adress,render_edit_butts(_.name)))) for _ in db["persons"]]
    tabs=[render_tr(map(render_th,HEADERS))]+tabs
    print TABLE % "".join(tabs)
    db.close()

def show_fail(warning):
    print FAIL %warning

def main():
    login()

if __name__ == '__main__':
    import cgitb; cgitb.enable(display=True)
    main()