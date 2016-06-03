'''
Created on May 28, 2014

@author: igor
'''
from chap6consts import *
from sqlobject.dbconnection import connectionForURI
from sqlobject.main import sqlhub, SQLObject
from sqlobject.col import StringCol, IntCol, FloatCol

LOGPATH = "ex14.log"
for_outer = setup_log(LOGPATH)

class User(SQLObject):
    __tablename__ = "users"
    usern = StringCol()
    passw = StringCol()

class Stocks(SQLObject):
    __tablename__ = "stocks"
    user = StringCol()
    stcomp = StringCol()
    stsym = StringCol()
    qua = IntCol()
    price = FloatCol()

class StockClass(object):
    
    def __init__(self):
        connection = connectionForURI("sqlite:/:memory:")
        sqlhub.processConnection = connection
        try:
            User.createTable()
            Stocks.createTable()
        except:
            pass
            
    def insert(self):
        st_price = get_current_price()
        portfolio = lambda user: ((user, stock, stsym, randint(1, 20), st_price[stsym]) 
                                  for stock, stsym 
                                  in STOCK_COMPS)
        [Stocks(**dict(zip(FIELDS_STOCKS, itm))) 
         for user in PERSONS for itm 
         in portfolio(user)]
        [User(usern=per, passw=per) 
         for per 
         in PERSONS]
    
    def login(self, usern, passw):
        res = User.select(User.q.usern == usern and User.q.passw == passw)
        return bool(list(res))
    
    def modify(self, user, stsym, newqua):
        for inst in Stocks.select(Stocks.q.user == user and Stocks.q.stsym == stsym):
            inst.set(qua=newqua)
            
    def update_price(self):
        st_price = get_current_price()
        for inst in Stocks.select():
            inst.price = st_price[inst.stsym]
            
    def get_tab_for_user(self, user):
        tab = Stocks.select(Stocks.q.user == user)
        return tab_to_html(tab)


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
