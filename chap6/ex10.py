'''
Created on May 25, 2014

@author: igor
'''
from Tkinter import Tk, Button, Label
from chap6listing import connect, insert, dbDump, delete, update, \
    create
import sqlite3

mybutton = Button
pack = lambda lst: map(lambda x: x.pack(), lst)

class Unshuffle(object):
    
    def __init__(self):
        self.top = Tk()
        self.db = ""
        self.cur = ""
        self.db_choices()
        self.top.mainloop()
        
    def db_choices(self):
        
        def set_db(t):
            self.db = sqlite3.connect(":memory:")  # connect(t, "test")
            self.db_which = t
            print(t)
            self.cur = self.db.cursor()
            create(self.cur)
            self.menu_choices()
            map(lambda x: x.pack_forget(), butts)
            
        butts = [mybutton(text=t, command=lambda t=t: set_db(t)) for t in ("sqlite", "gadfly", "mysql")]
        pack(butts)

    def menu_choices(self):
        
        def show(cur):
            cur.execute('SELECT * FROM users')
            db_data[0].config(text="")
            t = ('\n'.join(map(lambda x: "\t".join(map(str, x)), cur.fetchall())))
            db_data[0].config(text=t)
        
        choices = {
         # create":lambda:create(self.cur),
         "insert":lambda:insert(self.cur, self.db_which),
         "show":lambda :show(self.cur),
         "update":lambda : update(self.cur),
         "delete":lambda :delete(self.cur)
         }
        db_data = [Label()]
        butts = [mybutton(text=t, command=com) for t, com in choices.items()]
        pack(butts + db_data)

Unshuffle()    
