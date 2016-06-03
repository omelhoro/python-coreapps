'''
Created on May 28, 2014

@author: igor
'''
import pico
from time import ctime
import os
from random import randint
from functools import wraps
import urllib2
from distutils.log import warn as printf

STOCK_COMPS = (
             ("Microsoft", "MSFT"),
             ("Twitter", "TWTR"),
             ("Facebook", "FB"),
             ("Google", "GOOG"),
             ("Apple", "AAPL")
             )
STOCK_QUERY = "+".join(zip(*STOCK_COMPS)[1])
FIELDS_STOCKS = ("user", "stcomp", "stsym", "qua", "price")
FIELDS_LOGINS = ("user", "passw")
PERSONS = ("Igor", "Michael", "Wesley", "Vova")

LOGPATH="test.log"

def rand_generator(i,noti):
    while i==noti:
        return rand_generator(randint(1,5), noti)
    return i

def get_current_price():
    foo = urllib2.urlopen("http://finance.yahoo.com/d/quotes.json?s={}&f=sl1".format(STOCK_QUERY))
    st_price = dict((stnm, float(stsym)) 
                    for stnm, stsym in 
                    map(
                        lambda x: x.strip().replace("\"", "").split(","), 
                        foo.readlines()))
    return st_price


def setup_log(LOGPATH):
    
    #make sure a file exists or create it
    if os.path.isfile(LOGPATH):
        pass
    else:
        with open(LOGPATH, "w") as _:
            pass
    #write header for session
    with open(LOGPATH, "a") as f:
        f.write("Session {sid} started at {time}\n".format(
                                                           sid="".join(chr(randint(60, 120)) for _ in range(7)) , 
                                                           time=ctime()))

    #func for logging, should be used as decorator after suppling the logpath to setup_log:
    #>>>for_outer= setup_log("example.log")
    def for_outer(func):
        '''simple meta wrapper to log the call time, call func and the args'''
        @wraps(func)
        def wrapper(kwargs):
            with open(LOGPATH, "a") as f:
                vals = kwargs.values() if isinstance(kwargs, dict) else (kwargs,)
                ln = "{func} was called at {time} with args:{a}\n".format(
                                                                          func=func.func_name, 
                                                                          time=ctime(), 
                                                                          a=",".join(map(str, vals)))
                f.write(ln)
            try:
                res = func(**kwargs)
            except:
                res = func(kwargs)
            return res
        
        wrapper.__name__=func.__name__
        return wrapper

    return for_outer

        
def tab_to_html(tab):
    attrs_get = lambda obj: (getattr(obj, cat) for cat in FIELDS_STOCKS)
    td = lambda x: "<td>{x}</td>".format(x=x)
    tr = lambda x: "<tr>{x}</tr>".format(x=x)
    return "".join([tr("".join(map(td, attrs_get(r)))) for r in tab])

def setup(dbs):
    
    format_first_let= lambda nm:"({}){}".format(nm[0].upper(),nm[1:])
    valids={db[0]:db for db in dbs}
    tochoose="Choose the Database for testing:\n{}\n".format("\n".join(map(format_first_let,dbs)))
    choice=raw_input(tochoose).lower()
    if choice in valids:
        return valids[choice]
    else:
        print("Not a valid choice. Prompt again:")
        return setup(dbs)

def main(dbo):
    printf('\n*** Inserting names into table')
    dbo.insert()
    dbo.dbDump()

    printf('\n*** Randomly moving folks')
    fr, to, num = dbo.update()
    printf('\t(%d users moved) from (%d) to (%d)' % (num, fr, to))
    dbo.dbDump()

    printf('\n*** Randomly choosing group')
    rm, num = dbo.delete()
    printf('\t(group #%d; %d users removed)' % (rm, num))
    dbo.dbDump()

    printf('\n*** Dropping users table')
    dbo.drop()
    printf('\n*** Close cxns')
