'''
Created on May 30, 2014

@author: igor
'''
#!/usr/bin/env python

from distutils.log import warn as printf
from os.path import dirname
from random import randrange as rand
from sqlalchemy import Column, Integer, String, create_engine, exc, orm
from sqlalchemy.ext.declarative import declarative_base
from chap6listing import DBNAME, NAMELEN, randName,FIELDS, tformat, cformat, setup
from sqlalchemy import update as update1
from chap6consts import rand_generator

DSNs = {
    'mysql': 'mysql://root@localhost/%s' % DBNAME,
    'sqlite': 'sqlite:///:memory:',
}

Base = declarative_base()
class Users(Base):
    __tablename__ = 'users'
    login = Column(String(NAMELEN))
    userid   = Column(Integer, primary_key=True)
    projid  = Column(Integer)
    def __str__(self):
        return ''.join(map(tformat,
            (self.login, self.userid, self.projid)))

class SQLAlchemyTest(object):
    def __init__(self, dsn):
        try:
            eng = create_engine(dsn)
        except ImportError:
            raise RuntimeError()

        try:
            eng.connect()
        except exc.OperationalError:
            eng = create_engine(dirname(dsn))
            eng.execute('CREATE DATABASE %s' % DBNAME).close()
            eng = create_engine(dsn)

        Session = orm.sessionmaker(bind=eng)
        self.ses = Session()
        self.users = Users.__table__
        self.eng = self.users.metadata.bind = eng

    def insert(self):
        self.ses.add_all(
            Users(login=who, userid=userid, projid=rand(1,5)) \
            for who, userid in randName()
        )
        self.ses.commit()

    def update(self):
        fr = rand(1,5)
        to = rand_generator(rand(1,5), fr)
        foo=self.ses.query(Users).filter_by(projid=fr).update({"projid":to})
        #=================================================================================
        # users = self.ses.query(Users).filter_by(projid=fr).all()
        # for i, user in enumerate(users):
        #     user.projid = to
        #=================================================================================
        self.ses.commit()
        return fr, to, foo

    def delete(self):
        rm = rand(1,5)
        nusers = self.ses.query(Users).filter_by(projid=rm).delete()
        print nusers
        #=================================================================================
        # users = self.ses.query(Users).filter_by(projid=rm).all()
        # for i, user in enumerate(users):
        #     self.ses.delete(user)
        #=================================================================================
        self.ses.commit()
        return rm, nusers

    def dbDump(self,newest5=False,pyslice=False):
        printf('\n%s' % ''.join(map(cformat, FIELDS)))
        if newest5:
            if pyslice:
                users = self.ses.query(Users).order_by(Users.userid.desc()).all()[:5]
            else:
                users = self.ses.query(Users).order_by(Users.userid.desc()).limit(5)
        else:
            users = self.ses.query(Users).all()
        for user in users:
            printf(user)
        self.ses.commit()

    def __getattr__(self, attr):    # use for drop/create
        return getattr(self.users, attr)

    def finish(self):
        self.ses.connection().close()

def main():
    printf('*** Connect to %r database' % DBNAME)
    db = setup()
    if db not in DSNs:
        printf('\nERROR: %r not supported, exit' % db)
        return
    try:
        orm = SQLAlchemyTest(DSNs[db])
    except RuntimeError:
        printf('\nERROR: %r not supported, exit' % db)
        return

    printf('\n*** Create users table (drop old one if appl.)')
    orm.drop(checkfirst=True)
    orm.create()

    printf('\n*** Insert names into table')
    orm.insert()
    orm.dbDump()
    printf('\n*** Top 5 newest empls include')
    orm.dbDump(True)
    printf('\n*** Top 5 newest empls include, Pyslice')
    orm.dbDump(True,True)

    printf('\n*** Move users to a random group')
    fr, to, num = orm.update()
    printf('\t(%d users moved) from (%d) to (%d)' % (num, fr, to))
    orm.dbDump()

    printf('\n*** Randomly delete group')
    rm, num = orm.delete()
    printf('\t(group #%d; %d users removed)' % (rm, num))
    orm.dbDump()

    printf('\n*** Drop users table')
    orm.drop()
    printf('\n*** Close cxns')
    orm.finish()

if __name__ == '__main__':
    main()
   

