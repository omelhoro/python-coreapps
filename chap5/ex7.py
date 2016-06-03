'''
Created on May 14, 2014

@author: igor
'''
from Tkinter import Tk, Label, Button, StringVar, Entry, Toplevel

pack=lambda lst:[itm.pack() for itm in lst]


def enter_file(cur_file,label):
    print(cur_file.get())
    
    def read_file():
        try:
            with open(cur_file.get()) as f:
                label.config(text=f.read())
                fl_enter.destroy()
        except:
            label.config(text="No such file")

    fl_enter=Toplevel(top)
    qu_butts=[("Read",read_file),("Quit",lambda : fl_enter.destroy())]
    pack([Button(fl_enter,text=txt,command=f) for txt,f in qu_butts])
    pack([Entry(fl_enter,textvariable=cur_file)])
    fl_enter.mainloop()
        
top=Tk()
label=Label(top)
qu_butts=[("Open file",lambda: enter_file(cur_file,label)),("Quit",lambda : top.quit())]
START_STRING="/home/igor/txt.txt"


cur_file=StringVar()
cur_file.set(START_STRING)

lab_txt=StringVar()
pack([Button(text=txt,command=f) for txt,f in qu_butts])
pack([label])

top.mainloop()

