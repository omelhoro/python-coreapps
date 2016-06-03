'''
Created on May 14, 2014

@author: igor
'''
from Tkinter import Tk, Label, Button, StringVar, Entry, Toplevel, Text
from Tkconstants import INSERT, END
from collections import Counter
from _functools import partial
import re
from itertools import chain

pack=lambda lst:[itm.pack() for itm in lst]
menu_button=partial(Button,width=10,height=5/3,bg="white")
START_STRING="/home/igor/english_sample.txt"
#START_STRING="/home/igor/txt.txt"


def enter_file(cur_file,flnm_label,label,top):

    fl_enter=Toplevel(top)
    
    def read_file():
        flnm=cur_file.get()
        try:
            with open(flnm) as f:
                text=f.read()
        except:
            entry_field.config(background="red")
        label.delete("1.0",END)
        label.insert(INSERT,text)
        print("inserted",label)
        flnm_label.config(text=flnm)
        fl_enter.destroy()
    
    qu_butts=[("Read",read_file),("Cancel",fl_enter.destroy)]
    menu_buttons=[menu_button(master=fl_enter,text=txt,command=f) for txt,f in qu_butts]
    entry_field=Entry(fl_enter,textvariable=cur_file)

    pack(menu_buttons)
    pack([entry_field])
    fl_enter.mainloop()


def new_file(cur_file,flnm_label,label,top):
    fl_enter=Toplevel(top)
    
    def get_quit():
        flnm_label.config(text=cur_file.get())
        fl_enter.destroy()
    
    qu_butts=[("Make", get_quit),("Cancel",fl_enter.destroy)]
    
    menu_buttons=[menu_button(master=fl_enter,text=txt,command=f) for txt,f in qu_butts]
    entry_field=Entry(fl_enter,textvariable=cur_file)

    pack(menu_buttons)
    pack([entry_field])
    fl_enter.mainloop()

def save_file(cur_file,flnm_label,label,top,xt):

    def save():
        with open(cur_file.get(),"w+") as f:
            f.write(label.get("0.0",END))
    
    if xt:
        fl_enter=Toplevel(top)
        quit_question=Label(fl_enter,text="Do you want to save before quit?")
        steps=[fl_enter.quit]
        print([save]+steps)
        qu_butts=[
                  ("Cancel",fl_enter.destroy),
                  ("Save and quit", lambda: map(lambda x:x(),[save]+steps)),
                  ("Quit",lambda: map(lambda x:x(),steps))]
        menu_buttons=[menu_button(master=fl_enter,text=txt,command=f) for txt,f in qu_butts]
        pack([quit_question])
        pack(menu_buttons)
        fl_enter.mainloop()
    else:
        save()

dicts=("en.dict","2of12.txt")

with open(dicts[0]) as f:
    spell_dct={w.strip() for w in f.readlines()}


REG_SPLIT=re.compile(r"[ ,.?\"!\n\t']")
def spellchecker1(text_field):
    
    def find_word_ret_index(word,string,cur_find=None):
        cur_find=[] if cur_find is None else cur_find
        try:
            start_string=string.index(word)
            end_string=start_string+len(word)-1
            place_in_line=text[:start_string].rfind("\n")
            n_lines=string[:start_string].count("\n")+1
            if string[end_string+1] not in "[ (),.?\"!" or string[start_string-1] not in "[ (),.?\"!" :
                return find_word_ret_index(word, string[end_string+1:],cur_find)
            else:
                #print(word,string[start_string:start_string+7],string[start_string-1])
                l=["{0}.{1}".format(n_lines,start_string-place_in_line-1),
                        "{0}.{1}".format(n_lines,end_string-place_in_line)]
                print word,text_field.get(l[0],l[1]),l,string[start_string:start_string+7],text[:start_string].rfind("\n"),n_lines
                return find_word_ret_index(word, string[end_string:],cur_find+[l])
        except ValueError:
            #print("found",word,cur_find)
            return cur_find
        
    
    text=text_field.get("0.0",END)
    print text
    freq_dict=Counter(REG_SPLIT.split(text))

    fltr_f=lambda word: word.strip() not in spell_dct and word.strip().lower()  not in spell_dct and word
    add_falses=lambda start,end: text_field.tag_add("false",start,end)
    
    falses=[find_word_ret_index(word,text) for word in filter(fltr_f,freq_dict.iterkeys())]
    print(falses)
    [add_falses(*st_end) for st_end in chain(*falses)]
    text_field.tag_config("false",background="red")

def spellchecker(text_field):
    
    def find_word_ret_index1(word,string,cur_find,freq):
        if freq:
            start_string=string.index(word)
            end_string=start_string+len(word)-1
            place_in_line=text[:start_string].rfind("\n")
            n_lines=string[:start_string].count("\n")+1
            l=["{0}.{1}".format(n_lines,start_string-place_in_line-1),
                    "{0}.{1}".format(n_lines,end_string-place_in_line)]
            #print word,text_field.get(l[0],l[1]),l,string[start_string:start_string+7],text[:start_string].rfind("\n"),n_lines
            return find_word_ret_index(word, string[end_string:],cur_find+[l],freq-1)
        else:
            print("found",word,cur_find)
            return cur_find

    def find_word_ret_index(word,string,cur_find):
        lst=[]
        for i,ln in enumerate(splitted_text):
            ln_i=0
            while True:
                try:
                    start_string=ln.index(word)
                    end_string=start_string+len(word)
                    if ln[end_string] in "[ (),.?\"!" and ln[start_string-1] in "[ (),.?\"!":
                        l=["{0}.{1}".format(i+1,start_string+ln_i),
                            "{0}.{1}".format(i+1,end_string+ln_i)]
                        lst.append(l)
                    ln_i+=end_string
                    ln=ln[end_string:]
                except ValueError:
                    break
        return lst
    
    text=text_field.get("0.0",END)
    splitted_text=text.split("\n")

    fltr_f=lambda word: word.strip() not in spell_dct and word.strip().lower()  not in spell_dct and word
    add_falses=lambda start,end: text_field.tag_add("false",start,end)
    
    falses=[find_word_ret_index(word,text,[]) for word in filter(fltr_f,set(REG_SPLIT.split(text)))]
    [add_falses(*st_end) for st_end in chain(*falses)]
    text_field.tag_config("false",background="red")


def main():        
    top=Tk()
    text=Text(top)
    flnm_label=Label(top,text=START_STRING)
    
    qu_butts=[
              ("New File",lambda: new_file(*refs)),
              ("Open file",lambda: enter_file(*refs)),
              ("Save file",lambda: save_file(*refs,xt=False)),
              ("Spellcheck",lambda: spellchecker(text)),
              ("Quit",lambda: save_file(*refs,xt=True))]
    
    cur_file=StringVar()
    cur_file.set(START_STRING)

    with open(START_STRING) as f:
        text.insert(INSERT,f.read())
    
    menu_buttons=[menu_button(master=top,text=txt,command=f) for txt,f in qu_butts]

    pack(menu_buttons)
    pack([text,flnm_label])
    refs=(cur_file,flnm_label,text,top)
    top.mainloop()

main()