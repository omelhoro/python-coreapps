'''
Created on May 30, 2014

@author: igor
'''
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.types import Integer
from sqlalchemy.schema import Column
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

Base=declarative_base()


try:
    class Num(Base):
        __tablename__="nums"
        id = Column(Integer, primary_key=True)
        val=Column(Integer)
except:
    pass

def setup():
    try:
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine) 
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add_all((Num(val=i) for i in xrange(100)))
    except:
        pass
    return session

def change_upd():
    session=setup()
    session.query(Num).filter(Num.val%2==0).update({"val":3})

def change_for():
    session=setup()
    for nm in session.query(Num).filter(Num.val%2==0):
        nm.val=3

def delete_del():
    session=setup()
    session.query(Num).filter(Num.val%2==0).delete()

def delete_for():
    session=setup()
    for nm in session.query(Num).filter(Num.val%2==0):
        session.delete(nm)



#=========================================================================================
# %timeit delete_for()
# %timeit delete_del()
# 
# %timeit change_for()
# %timeit change_upd()
#=========================================================================================
session=setup()
usrtab=Num.__table__
len(session.query(Num).filter(Num.val%2==0).all())
usrtab.update().where(Num.val%2==0).values(val=3)
len(session.query(Num).filter(Num.val%2==0).all())

sumsor=map(lambda x: len(session.query(Num).filter(Num.val%x==0).all()),range(10,20))
sums=sumsor[:]
from operator import sub,add
reduce(lambda a,b: map(lambda x: add(*x), zip(a,a[1:])),range(len(sums)-1),sums)
for i in range(len(sums)):
    sums=map(lambda x: sub(*x), zip(sums,sums[1:]))
    print sums
    