'''
Created on May 30, 2014

@author: igor
'''
#!/usr/bin/env python
from distutils.log import warn as printf
from os.path import dirname
from random import randrange as rand
from sqlalchemy import Column, Integer, String, create_engine, exc, orm, MetaData, Table,insert
from chap6listing import DBNAME, NAMELEN, randName, FIELDS, tformat, cformat, setup
from sqlalchemy.orm.session import sessionmaker

DSNs = {
     'mysql': 'mysql://root@localhost/%s' % DBNAME,
    'sqlite': 'sqlite:///:memory:',
}

class SQLAlchemyTest(object):
    def __init__(self, dsn):
        try:
            eng = create_engine(dsn)
        except ImportError, _:
            raise RuntimeError()

        try:
            cxn = eng.connect()
        except exc.OperationalError:
            try:
                eng = create_engine(dirname(dsn))
                eng.execute('CREATE DATABASE %s' % DBNAME).close()
                eng = create_engine(dsn)
                cxn = eng.connect()
            except exc.OperationalError:
                raise RuntimeError()

        metadata = MetaData()
        self.eng = metadata.bind = eng
        try:
            users = Table('users', metadata, autoload=True)
        except exc.NoSuchTableError:
            users = Table('users', metadata,
                Column('login',  String(NAMELEN)),
                Column('userid', Integer),
                Column('projid', Integer),
            )

        self.session=sessionmaker(bind=self.eng)()
        self.cxn = cxn
        self.users = users

    def insert(self):
        d = [dict(zip(FIELDS, [who, uid, rand(1,5)]))
            for who, uid in randName()]
        
        #return insert(self.users,values=d)
        return self.users.insert().execute(*d).rowcount

    def update(self):
        users = self.users
        fr = rand(1,5)
        to = rand(1,5)
        return (fr, to,
            users.update(users.c.projid==fr).execute(projid=to).rowcount)

    def delete(self):
        users = self.users
        rm = rand(1,5)
        return (rm,
            users.delete(users.c.projid==rm).execute().rowcount)

    def dbDump(self):
        printf('\n%s' % ''.join(map(cformat, FIELDS)))
        users = self.users.select().execute()
        for user in users.fetchall():
            printf(''.join(map(tformat, (user.login,user.userid, user.projid))))

    def __getattr__(self, attr):
        return getattr(self.users, attr)

    def finish(self):
        self.cxn.close()

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
