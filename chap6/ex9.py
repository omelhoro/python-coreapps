'''
Created on May 25, 2014

@author: igor
'''
# ex9.py
import pico
import sqlite3
from random import randint



def insert(cur, db):
    if db == 'sqlite':
        cur.executemany("INSERT INTO users VALUES(?, ?, ?)",
        [(who, uid, randint(1, 5)) for who, uid in NAMES])

def create(cur):
    cur.execute('''
       CREATE TABLE users (
         login  VARCHAR(%d),
         userid INTEGER,
         projid INTEGER)
    ''' % 10)

NAMES = (
    ('aaron', 8312), ('angela', 7603), ('dave', 7306),
    ('davina', 7902), ('elliot', 7911), ('ernie', 7410),
    ('jess', 7912), ('jim', 7512), ('larry', 7311),
    ('leslie', 7808), ('melissa', 8602), ('pat', 7711),
    ('serena', 7003), ('stan', 7607), ('faye', 6812),
    ('amy', 7209), ('mona', 7404), ('jennifer', 7608),
)

db = sqlite3.connect(":memory:")  # @UndefinedVariable
cur = db.cursor()
create(cur)
insert(cur, "sqlite")

def show(cr="ii"):
    
    def tab_to_html(tab):
        td = lambda x: "<td>{x}</td>".format(x=x)
        tr = lambda x: "<tr>{x}</tr>".format(x=x)
        return "".join([tr(map(td, r)) for r in tab])

    cur.execute("SELECT * FROM users")
    return tab_to_html(cur.fetchall())

def update(cr="foo"):
    
    fr = randint(1, 5)
    to = randint(1, 5)
    cur.execute(
     "UPDATE users SET projid=%d WHERE projid=%d" % (to, fr))

def delete(cr="foo"):
    rm = randint(1, 5)
    cur.execute('DELETE FROM users WHERE projid=%d' % rm)

def insert_new():
    insert(cur,"sqlite")
    