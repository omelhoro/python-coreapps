'''
Created on May 27, 2014

@author: igor
'''
from itertools import chain
import sqlite3
from chap6consts import *

LOGPATH = "ex11.log"

for_outer=setup_log(LOGPATH)

def setup():
    
    st_price = get_current_price()
    portfolio = lambda user: ((user, stock, stsym, randint(1, 20), st_price[stsym]) for stock, stsym in STOCK_COMPS)
    
    db = sqlite3.connect(":memory:")  # @UndefinedVariable
    cur = db.cursor()
    cur.execute("""CREATE TABLE stocks (
                                      user VARCHAR(15),
                                      stcomp VARCHAR(20),
                                      stsym VARCHAR(8),
                                      qua INTEGER,
                                      price REAL
                                      ) """)
    
    cur.executemany("INSERT INTO stocks VALUES (?,?,?,?,?) ", chain(*[portfolio(user) for user in PERSONS]))

    # login table
    cur.execute("""CREATE TABLE logins ( 
                                    usern VARCHAR(15),
                                    passw VARCHAR(20)
                                      )""")
    cur.executemany("INSERT INTO logins VALUES (?,?)", ((nm, nm) for nm in PERSONS))
    return db, cur

for_outer=setup_log(LOGPATH)
db, cur = setup()


@for_outer
def login(usern, passw):
    cur.execute("SELECT * FROM logins WHERE usern=? AND passw=?", (usern, passw))
    return bool(cur.fetchall())
    
@for_outer
def get_users():
    to_button = lambda x: "<button class='user' value='{0}'>{0}</button>".format(x)
    return "<div>{}</div>".format("".join(map(to_button, PERSONS)))

@for_outer
def update_price(foo):
    st_price = get_current_price()
    cur.executemany("UPDATE stocks SET price=? WHERE stsym=?", [tpl[::-1] for tpl in st_price.iteritems()])

@for_outer
def modify(user, stsym, plus, curqua):
    newqua = int(curqua) + 1 if plus else int(curqua) - 1
    cur.execute("UPDATE stocks SET qua=? WHERE user=? AND stsym=? ", (newqua, user, stsym))
    
@for_outer
def get_tab_for_user(user):

    def tab_to_html(tab):
        td = lambda x: "<td>{x}</td>".format(x=x)
        tr = lambda x: "<tr>{x}</tr>".format(x=x)
        return "".join([tr("".join(map(td, r))) for r in tab])
    
    cur.execute("SELECT * FROM stocks WHERE user=?", (user,))
    return tab_to_html(cur.fetchall()) 

from ctypes import *
from ctypes import cdll
mydll = cdll.LoadLibrary('statslib.so')
mylib = CDLL("hello.so")

