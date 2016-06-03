'''
Created on May 14, 2014

@author: igor
'''
from Tkinter import Tk, Label, Button

top=Tk()
label=Label(top, text="Omelhoro e o melhor")
butts_txt=["Omelhoro e o melhor","Igor is the best",u"Игорь самый лучший."]

make_butt=lambda lab,txt:Button(top,text=txt, command=lambda: lab.config(text=txt))
butts=[make_butt(label,txt) for txt in butts_txt]
[b.pack() for b in butts]
label.pack()
top.mainloop()