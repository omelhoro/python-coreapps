'''
Created on May 30, 2014

@author: igor
'''
from storm.properties import Int, Unicode
from storm.database import create_database
from storm.store import Store, ResultSet
from chap6listing import randName
from random import randint
from chap6consts import rand_generator,main, setup
from chap6listing import tformat

class User(object):
    __storm_table__="users"
    id= Int(primary=True)
    login=Unicode()
    userid=Int()
    projid=Int()
    
    def __init__(self,id,login,userid,projid):
        self.id=id
        self.login=login
        self.userid=userid
        self.projid=projid

    def __str__(self):
        return ''.join(map(tformat,(self.login, self.userid, self.projid)))



class Storm(object):
    
    def __init__(self,db="sqlite"):
        uname="root"
        passw=""
        if db=="postgres":
            passw="root"
        elif db=="sqlite":
            expr="sqlite:"
        if db!="sqlite":
            expr="{db}://{usern}:{passw}@localhost/test".format(db=db,usern=uname,passw=passw)
        self.database = create_database(expr)
        self.store = Store(self.database)
        #self.store.execute("DROP TABLE users")
        self.store.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, login VARCHAR(8), userid INTEGER, projid INTEGER)")
        
        
    def insert(self):
        users=(User(id=userid,login=unicode(who), userid=userid, projid=randint(1,5)) for who, userid in randName())
        map(self.store.add,users)
    
    def update(self):
        fr=randint(1,5)
        to=rand_generator(randint(1,5),fr)
        q=self.store.find(User, User.projid == fr)
        c=q.count()
        q.set(projid=to)
        return fr,to,c

    def delete(self):
        fr=randint(1,5)
        q=self.store.find(User, User.projid == fr)
        c=q.count()
        q.remove()
        return fr,c

    def drop(self):
        pass
    
    def dbDump(self):
        for i in self.store.find(User):
            print i
ResultSet

choice=setup(("postgres","mysql","sqlite"))
dbo=Storm()
main(dbo)