'''
Created on May 27, 2014

@author: igor
'''
from chap6consts import *  
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.types import String, Integer, Float
from sqlalchemy.schema import Column
from sqlalchemy.orm.session import sessionmaker

LOGPATH = "ex13.log" 

Base = declarative_base()
for_outer=setup_log(LOGPATH)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    usern = Column(String)
    passw = Column(String)


class Stocks(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    user = Column(String)
    stcomp = Column(String)
    stsym = Column(String)
    qua = Column(Integer)
    price = Column(Float)


class StockClass(object):
    
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
    
    def insert(self):
        st_price = get_current_price()
        portfolio = lambda user: ((user, stock, stsym, randint(1, 20), st_price[stsym]) 
                                  for stock, stsym 
                                  in STOCK_COMPS)
        user_data = (Stocks(**dict(zip(FIELDS_STOCKS, itm))) 
                     for user in PERSONS 
                     for itm in portfolio(user))
        self.add_all(user_data)
        
        logins = (User(usern=per, passw=per) for per in PERSONS)
        self.add_all(logins)
    
    def login(self, usern, passw):
        res = self.query(User).filter_by(usern=usern, passw=passw)
        return bool(list(res))
    
    def update_price(self):
        st_price = get_current_price()
        for inst in self.query(Stocks):
            inst.price = st_price[inst.stsym]

    def modify(self, user, stsym, newqua):
        for inst in self.query(Stocks).filter_by(stsym=stsym):
            inst.qua = newqua
    
    def get_tab_for_user(self, user):
        tab = self.query(Stocks).filter_by(user=user)
        return tab_to_html(tab)

    def __getattr__(self, attr):
        return getattr(self.session, attr)

 
@for_outer
def login(usern, passw):
    return dba.login(usern, passw)

@for_outer
def update_price(foo):
    return dba.update_price()

@for_outer
def modify(user, stsym, plus, curqua):
    newqua = int(curqua) + 1 if plus else int(curqua) - 1
    return dba.modify(user, stsym, newqua)

@for_outer
def get_tab_for_user(user):
    return dba.get_tab_for_user(user)

dba = StockClass()       
dba.insert() 


