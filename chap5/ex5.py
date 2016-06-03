#encoding=utf8
'''
Created on May 14, 2014

@author: igor
'''
from Tkinter import Tk, Label, Button, Radiobutton, StringVar

top=Tk()
label=Label(top)
rbutts_txt=["Omelhoro e o melhor","Igor is the best",u"Игорь самый лучший."]
qu_butts=[("Update",lambda: label.config(text=lab_txt.get())),("Quit",lambda : top.quit())]




pack=lambda lst:[itm.pack() for itm in lst]
make_butt=lambda lab,txt:Radiobutton(top,text=txt,variable=lab_txt,value=txt,command=lambda:lab_txt.set(txt))

lab_txt=StringVar()
pack([make_butt(label,txt) for txt in rbutts_txt])
pack([Button(text=txt,command=f) for txt,f in qu_butts])
pack([label])

top.mainloop()