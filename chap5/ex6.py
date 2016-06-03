'''
Created on May 14, 2014

@author: igor
'''

from Tkinter import Tk, Label, Button, Radiobutton, StringVar, Entry

top=Tk()
label=Label(top)
qu_butts=[("Update",lambda: label.config(text=lab_txt.get())),("Quit",lambda : top.quit())]
start_string="Hello World"



pack=lambda lst:[itm.pack() for itm in lst]

lab_txt=StringVar()



pack([Button(text=txt,command=f) for txt,f in qu_butts])
pack([label])
lab_txt.set(start_string)
label.config(text=start_string)

pack([Entry(textvariable=lab_txt)])

top.mainloop()