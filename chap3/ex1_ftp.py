'''
Created on Apr 23, 2014

@author: igor
'''
from ftplib import FTP as ftp  
import os

update_files={
              "praat":("praat5372_linux32.tar.gz","ftp.u-aizu.ac.jp","/pub/misc/praat/"),
              "skype":("libqt4-webkit_4.6.3-4+squeeze1_i386.deb","ftp.us.debian.org","/debian/pool/main/q/qt4-x11/"),
              "firefox":("firefox-28.0.tar.bz2","ftp.mozilla.org","/pub/mozilla.org/firefox/releases/28.0/linux-x86_64/en-US")
              }

os.chdir("/home/igor/tmp/")
def get_new_software():
    for fn,ad,dr in update_files.values():
        print("login to {}".format(ad))
        ft=ftp(ad)
        ft.login()
        print("change to {}".format(dr))
        ft.cwd(dr)
        print("download {}".format(fn))
        with open(fn,"wb") as f:
            ft.retrbinary('RETR %s' % fn, f.write)
    print("done")
get_new_software()