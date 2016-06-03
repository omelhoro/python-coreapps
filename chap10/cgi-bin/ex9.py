#!/usr/bin/env python
# encoding=utf8
'''
Created on Jun 17, 2014

@author: igor
'''
import cgi
import shelve
import os
import Cookie
from time import ctime
from datetime import time
from random import randint

format_url = lambda x: "/cgi-bin/ex9.py?action={}".format(x)


DPATH = "cgi-bin/data/"
DFL = "ex9.dat"

class Item(object):
    
    def __init__(self, **kwargs):  # name,descp,price,cat,stock
        self.__dict__.update(kwargs)
        
    def renderitem(self):
        item_tml = "<li class='item' >%s<ul>%s</ul></li>"
        desc_tml = "<li class='%s' >%s</li>"
        desc = map(lambda x: desc_tml % (x, getattr(self, x)), itemattrs[1:])  # without name
        return item_tml % (self.name, "".join(desc))
        

class ShoppingCart(object):  # dynamic model
    
    def __init__(self):
        self.items = []

class User(object):  # model
    
    @classmethod
    def toshc(self, logged, cls):
        ITEMSHC = SCTT("""<span class='success'>Item now in shopping cart</span>
                            <p>
                            <a href=%s>To main page</a>
                            <a href=%s>To buy page</a>
                            </p>"""
                            )

        db = access_db(True)
        ulogged = Logging.get_logged_user()
        uclass = next(x for x in db["users"] if x.usern == ulogged)
        try:
            product = next(x for x in db["products"] if x.name == cls.replace("_"," "))
        except StopIteration:
            print(SCTT(cls))
            return None
        else:
            uclass.addshc(product)
        finally:
            db.close()
        
        print(ITEMSHC % (format_url(""), format_url("uinf" + uclass.usern)))
        
    @classmethod
    def dropi(self,stat,item):
        db = access_db(True)
        ulogged = Logging.get_logged_user()
        uclass = next(x for x in db["users"] if x.usern == ulogged)
        uclass.dropitem(item)
        print(uclass.info())
        db.close()
        
        
    @classmethod
    def buyall(self,stat,cls):
        BOUGHT= SCTT("""
                        <span class='success'>All items bought</span>
                        <p>
                        <a href=%s>To main page</a>
                        </p>""" % format_url(""))
    
        
        db = access_db(True)
        ulogged = Logging.get_logged_user()
        uclass = next(x for x in db["users"] if x.usern == ulogged)
        uclass.buyalla()
        db.close()
        print(BOUGHT)
        
    @classmethod
    def showinfo(self, stat, cls):
        db = access_db()
        uclass = next(x for x in db["users"] if x.usern == cls)
        print(uclass.info())
    
    def __init__(self, usern, passw):
        self.usern = usern
        self.passw = passw
        self.shcard = ShoppingCart()
        self.bought = []

    def info(self):
        UINFO = SCTT("In shopping card: <ol>%s</ol><p>already bought:<ol>%s</ol> </p> <p><a href=%s ><button>Buy all</button></a></p>")

        renderlist = lambda y:"".join(map(lambda x:"<li>{}</li>".format(x), y))
        rendershc = lambda y:"".join(map(lambda x:"<li>{0}<a href={1}><button>Drop</button></a> </li>".format(x,format_url("droi"+x)), y))
        print UINFO % (rendershc(self.shcard.items), renderlist(self.bought), format_url("buya"+self.usern))
    
    def addshc(self, product):
        self.shcard.items.append(product.name)
    
    def dropitem(self,item):
        self.shcard.items.remove(item)
    
    def buyalla(self):
        shc=self.shcard.items
        self.bought.extend(shc)
        self.shcard=ShoppingCart()

itemattrs = ("name", "descp", "price", "cat", "stock")
itms = [("Ventilator", "keeps really cool by venting", 300, "house", 10),
("Bike", "superfast, for mountains", 500, "sports", 3),
("Ipod", "nice music quality by apple", 100, "electronic", 1),
("Lenovo Laptop", "fast i7 processor", 532, "electronic", 10),
("Jacket", "warm for outdoors", 23, "clothing", 2),
("Basketball", "bounces badly", 3, "sports", 14),
("Desktop by HP", "fast and expansible desktop", 555, "electronic", 3),
("Picture of a Tree", "wonderful,high quality landscape from Brazil ", 20, "house", 10)]

userattrs = ("usern", "passw")
usrs = (("if154", "igor"), ("fi154", "bolt"))

def create_db():
    d = shelve.open(DPATH + DFL)
    d["products"] = map(lambda x:Item(**dict(zip(itemattrs, x))), itms)
    d["users"] = map(lambda x:User(**dict(zip(userattrs, x))), usrs)
    d.close()

if DFL not in os.listdir(DPATH):
    create_db()




def access_db(writeback=False):
    d = shelve.open(DPATH + DFL, writeback=writeback)
    return d
    

class Logging(object):
    

    @classmethod
    def renderlogin(self, warn=""):
        LOGIN = SCTT("""%s
            <form method=post action=%s>
            Username <input type="text"name='usern' value="if154" ><br>
            Password <input type="password" name='passw' value="igor" ><br>
            <input type="submit"><br>
            </form>
            """ % ("%s", format_url("cntr")))
        print(LOGIN % warn)
    
    @classmethod
    def auth(self, form):
        db = access_db()
        usern, upass = form["usern"].value, form["passw"].value
        try:
            user = next(x for x in db["users"] if x.usern == usern)
        except StopIteration:
            Logging.renderlogin("No such username")
        else:
            if user.passw == upass:
                Logging.set_cookie(usern)
                print(SCTT("<span class='success'> Login successful</span> <a href='/cgi-bin/ex9.py'>Main page </a>"))
            else:
                Logging.renderlogin("Wrong password")
                
    @classmethod
    def set_cookie(self, usern):
        hascookie, cookie_string = Logging.get_cookie()
        if not cookie_string:
            c = Cookie.SimpleCookie()
            c["token"] = "{}".format(usern)
            print c
    
    @classmethod
    def get_logged_user(self):
        has_cookie, string = Logging.get_cookie()
        return string.replace("token=", "")
    
    @classmethod
    def getstatus(self):
        loginbut = "<a href={}><button>Login</button></a>".format(format_url("logi")) 
        userlogged = "<span>Logged in as <a href=%s><button>%s</button></a><a href={}><button>Logout</button></a>".format(format_url("logo"))
        has_cookie, string = Logging.get_cookie()
        string = string.replace("token=", "")
        userstat = loginbut if not has_cookie else userlogged % (format_url("uinf" + string), string.title())
        return userstat
    
    @classmethod
    def logout(*args):
        c = Cookie.SimpleCookie()
        c["token"]="foo"
        c["token"]["max-age"]=0.0
        print(c)
        print(SCTT())
        

    @classmethod
    def get_cookie(self):
        cookie_string = os.environ.get('HTTP_COOKIE')
        return (bool(cookie_string), cookie_string)

SCTT1 = """
<html>
<head>
<title>%s</title>
<link type='text/css' href='/media/gen.css' rel='stylesheet'></link>
</head>
<body>
%s
</body>
</html>"""

def cats():
    db = access_db()
    cats = { x.cat for x in db["products"]}  # set of all cats
    db.close()
    render_link = lambda x: "<span><a class='cat' href={0}>{1}</a></span>".format(format_url("show" + x), x.title())
    return "".join(map(render_link, cats))

SCTT=lambda x="":SCTT1 %("Main", "<nav class=tier1>{0}</nav><nav class=tier2>{1}</nav>%s".format(Logging.getstatus(),cats())) %x

class WebShop(object):  # view

    #MAIN = SCTT() % %s")
    
    def __init__(self, form):
        self.actions = {
                        "droi":User.dropi,
                        "buya":User.buyall,
                        "buyi":User.toshc,
                      "show": self.showcat,
                      "uinf": User.showinfo,
                      "logi":lambda *x: Logging.renderlogin(),
                      "logo":lambda *x: Logging.logout(),
                      "cntr":lambda *x: Logging.auth(form)
                      } 
        self.process(form)
    
    def process(self, form):
        try:
            action = form["action"].value
        except KeyError:
            self.showmain()
        else:
            actype, spec = action[:4], action[4:]
            userstat, _ = Logging.get_cookie()
            viewfn = self.actions.get(actype, self.showmain)
            viewfn(userstat, spec)
            
    def showcat(self, userstat, cat):
        items_tml = "<ol>%s<ol>"
        buyitem = lambda x: "<a href=%s ><button>Buy</button></a>" % format_url("buyi" + x.replace(" ","_")) if userstat else ""
        
        db = access_db()
        itms_of_cat = filter(lambda x: x.cat == cat, db["products"])
        db.close()
        
        lst = map(lambda x: x.renderitem() + buyitem(x.name), itms_of_cat)
        print(SCTT(items_tml % "".join(lst)))
        
    def showmain(self):
        print(SCTT())




 

if __name__ == '__main__':
    import cgitb; cgitb.enable(display=True)
    form = cgi.FieldStorage()
    WebShop(form)

#=========================================================================================
# import shelve
# p="/home/igor/workspace_scala/Book-Python-Coreapps/chap10/cgi-bin/data"
# d=shelve.open(p+"/ex9.dat")
# d
# d.close()
# 
# def create_db():
#     d = shelve.open(p + "/ex9.dat")
#     d["products"] = map(lambda x:Item(**dict(zip(itemattrs, x))), itms)
#     d["users"] = map(lambda x:User(**dict(zip(userattrs, x))), usrs)
#     d.close()
# 
# create_db()
#=========================================================================================
