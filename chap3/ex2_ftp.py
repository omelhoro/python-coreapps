'''
Created on Apr 28, 2014

@author: igor
'''

from ftplib import FTP as ftp
import os
import ftplib

user="igor"
passwd="8089080"
ad='localhost'

root="/home/igor/tmp/"
goal="/home/igor/tmp/ftp"
def get_new_software():
    print("login to {}".format(ad))
    ft=ftp(ad)
    ft.login(user, passwd)
    ft.cwd(root)
    cur_flist=ft.nlst()
    print(cur_flist)
    while True:
        pat=raw_input("Pattern to move: ")
        if pat.startswith("*"):
            subset=[f for f in cur_flist if f.endswith(pat[1:])]
        else:
            subset=[f for f in cur_flist if f.startswith(pat)]
        for fn in subset:
            with open("{goal}/{fn}".format(goal=goal,fn=fn),"wb") as f:
                print(fn)
                try:
                    ft.retrbinary("RETR {fn}".format(fn=fn), f.write)
                except ftplib.error_perm:
                    print("Not a binary file!")
    print("done")
    ft.quit()
get_new_software()
