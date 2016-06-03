'''
Created on May 28, 2014

@author: igor
'''
#=========================================================================================
# import MySQLdb
# 
# DBUSER="root"
# DBNAME="test"
# 
# with MySQLdb.connect(user=DBUSER) as cxn:
#     cxn = MySQLdb.connect(user=DBUSER)
#     cxn.query('CREATE DATABASE %s' % DBNAME)
#     cxn.commit()
#     cxn.close() 
#     cxn = MySQLdb.connect(db=DBNAME)
#     #cxn.query('DROP DATABASE %s' % DB)
#     #cxn.query('CREATE DATABASE %s' % DB)
# 
# 
# with MySQLdb.connect("localhost",DBUSER,"",DBNAME) as cxn:
#     pass
# 
#     
# import psycopg2 as psql
# cxn = psql.connect("dbname='postgres' user=igor host = 'localhost' password='igor'")
# cxn.set_isolation_level(0)
# cur=cxn.cursor()
# cur.execute("""DROP DATABASE test;""")
# cur.execute("""CREATE DATABASE test;""")
# cur.close()
# cxn.close()
# 
# try:
#     cur.execute("""CREATE DATABASE test;""")
# except:
#     cur.execute("""DROP DATABASE test;""")
#     cur.execute("""CREATE DATABASE test;""")
# cur.close()
# cxn.close()
# 
# 
# cxn = psql.connect("dbname='test' user=igor host = 'localhost' password='igor'")
# 
# cxn=psql.connect(database="test",host="localhost", user="root",password="root")
# cur=cxn.cursor()
# 
# #cur.execute("""DROP DATABASE test;""")
# #cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
# cur.execute("SELECT * FROM test;")
# cur.fetchall()
# 
# cur.close()
# cxn.commit()
# cxn.close()
#=========================================================================================

#!/usr/bin/env python

from distutils.log import warn as printf
import os
from random import randrange as rand

if isinstance(__builtins__, dict) and 'raw_input' in __builtins__:
    scanf = raw_input
elif hasattr(__builtins__, 'raw_input'):
    scanf = raw_input
else:
    scanf = input

COLSIZ = 10
FIELDS = ('login', 'userid', 'projid')
RDBMSs = {'s': 'sqlite', 'm': 'mysql', 'g': 'gadfly','p':"postgres"}
DBNAME = 'test'
DBUSER = 'root'
DB_EXC = None
NAMELEN = 16
DBPASS= DBUSER

tformat = lambda s: str(s).title().ljust(COLSIZ)
cformat = lambda s: s.upper().ljust(COLSIZ)

def setup():
    return RDBMSs[raw_input('''
Choose a database system:

(M)ySQL
(G)adfly
(S)QLite
(P)ostgres

Enter choice: ''').strip().lower()[0]]

def connect(db, DBNAME=DBNAME):
    global DB_EXC
    dbDir = '%s_%s' % (db, DBNAME)
    printf(dbDir)

    if db == 'sqlite':
        try:
            import sqlite3
        except ImportError:
            try:
                from pysqlite2 import dbapi2 as sqlite3
            except ImportError:
                return None

        DB_EXC = sqlite3
        if not os.path.isdir(dbDir):
            os.mkdir(dbDir)
        cxn = sqlite3.connect(os.path.join(dbDir, DBNAME))

    elif db == 'mysql':
        try:
            import MySQLdb
            import _mysql_exceptions as DB_EXC
            try:
                cxn = MySQLdb.connect(db=DBNAME)
            except DB_EXC.OperationalError:
                try:
                    cxn = MySQLdb.connect(user=DBUSER)
                    cxn.query('DROP DATABASE %s' % DBNAME)
                    cxn.query('CREATE DATABASE %s' % DBNAME)
                    cxn.commit()
                    cxn.close() 
                    cxn = MySQLdb.connect("localhost",DBUSER,"",DBNAME)
                except DB_EXC.OperationalError:
                    return None
        except ImportError:
            try:
                import mysql.connector
                import mysql.connector.errors as DB_EXC
                try:
                    cxn = mysql.connector.Connect(**{
                        'database': DBNAME,
                        'user': DBUSER,
                    })
                except DB_EXC.InterfaceError:
                    return None
            except ImportError:
                return None

    elif db == 'gadfly':
        try:
            from gadfly import gadfly
            DB_EXC = gadfly
        except ImportError:
            return None
    
        try:
            cxn = gadfly(DBNAME, dbDir)
        except IOError:
            cxn = gadfly()
            if not os.path.isdir(dbDir):
                os.mkdir(dbDir)
            cxn.startup(DBNAME, dbDir)

    elif db == 'postgres':
        try:
            import psycopg2 as psql
            DB_EXC = psql
        except ImportError:
            return None
        
        #create brandnew dbase
        cxn = psql.connect(database='postgres', user=DBUSER, host = 'localhost', password=DBPASS)
        cxn.set_isolation_level(0)
        cur=cxn.cursor()
        cur.execute("DROP DATABASE test;")
        cur.execute("CREATE DATABASE test;")
        cur.close()
        cxn.close()
        cxn = psql.connect(database=DBNAME,host="localhost", user=DBUSER,password=DBPASS)
    else:
        return None

    return cxn

def create(cur):
    try:
        cur.execute('''
           CREATE TABLE users (
             login  VARCHAR(%d),
             userid INTEGER,
             projid INTEGER)
        ''' % NAMELEN)
    except DB_EXC.OperationalError, _:
        drop(cur)
        create(cur)

drop = lambda cur: cur.execute('DROP TABLE users')

NAMES = (
    ('aaron', 8312), ('angela', 7603), ('dave', 7306),
    ('davina',7902), ('elliot', 7911), ('ernie', 7410),
    ('jess', 7912), ('jim', 7512), ('larry', 7311),
    ('leslie', 7808), ('melissa', 8602), ('pat', 7711),
    ('serena', 7003), ('stan', 7607), ('faye', 6812),
    ('amy', 7209), ('mona', 7404), ('jennifer', 7608),
)

def randName():
    pick = set(NAMES)
    while pick:
        yield pick.pop()

def insert(cur, db):
    print(db)
    if db == 'sqlite':
        cur.executemany("INSERT INTO users VALUES(?, ?, ?)",
        [(who, uid, rand(1,5)) for who, uid in randName()])
    elif db == 'gadfly':
        for who, uid in randName():
            cur.execute("INSERT INTO users VALUES(?, ?, ?)",(who, uid, rand(1,5)))
    elif db in ('mysql',"postgres"):
        cur.executemany("INSERT INTO users VALUES(%s, %s, %s)", [(who, uid, rand(1,5)) for who, uid in randName()])

getRC = lambda cur: cur.rowcount if hasattr(cur,"owcount") else -1

def update(cur):
    
    def rand_generator(i,noti):
        while i==noti:
            return rand_generator(rand(1,5), noti)
        return i
    
    fr = rand(1,5)
    to = rand_generator(rand(1,5), fr)
    cur.execute(
     "UPDATE users SET projid=%d WHERE projid=%d" % (to, fr))
    return fr, to, getRC(cur)

def delete(cur):
    rm = rand(1,5)
    cur.execute('SELECT * FROM users WHERE projid=%d' % rm)
    if cur.fetchone():
        cur.execute('DELETE FROM users WHERE projid=%d' % rm)
        return rm, getRC(cur)
    else:
        return delete(cur)

def dbDump(cur):
    cur.execute('SELECT * FROM users')
    printf('\n%s' % ''.join(map(cformat, FIELDS)))
    for data in cur.fetchall():
        printf(''.join(map(tformat, data)))

def main():
    db = setup()
    printf('*** Connect to %r database' % db)
    cxn = connect(db)
    if not cxn:
        printf('ERROR: %r not supported or unreachable, exit' % db)
        return
    cur = cxn.cursor()

    printf('\n*** Creating users table')
    create(cur)

    printf('\n*** Inserting names into table')
    insert(cur, db)
    dbDump(cur)

    printf('\n*** Randomly moving folks')
    fr, to, num = update(cur)
    printf('\t(%d users moved) from (%d) to (%d)' % (num, fr, to))
    dbDump(cur)

    printf('\n*** Randomly choosing group')
    rm, num = delete(cur)
    printf('\t(group #%d; %d users removed)' % (rm, num))
    dbDump(cur)

    printf('\n*** Dropping users table')
    drop(cur)
    printf('\n*** Close cxns')
    cur.close()
    cxn.commit()
    cxn.close()

if __name__ == '__main__':
    main()

