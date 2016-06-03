#!/usr/bin/env python
# encoding=utf8
'''
Created on Jun 15, 2014

@author: igor
'''
import cgi
import os
from StringIO import StringIO
import tarfile
START = """
<html>
<head><title>Login form</title></head>
<body>
%s
<form method=post ENCTYPE="multipart/form-data">
File<input type="file" name='upfile'><br>
<input type='submit' >
</form>
</body>
</html>"""

SUCC = """
<html>
<head><title>Main Site</title></head>
<body>
Upload successful!
</body>
</html>"""

FAIL="""
<html>
<head><title>Main Site</title></head>
<body>
File archive not supported!
</body>
</html>"""

#=========================================================================================
# from gzip import GzipFile
# from StringIO import StringIO
# with open("bookmarkslinuxPort.html.gz") as fl:
#     flcont=StringIO(fl.read())
#     f_ar=GzipFile(fileobj=flcont)
#     with open("test","wb") as f:
#         f.write(f_ar.read())
# 
# import os
# #os.path.splitext("bookmarkslinuxPort.html.zip")
#=========================================================================================

PATH="cgi-bin/data/"

def upload(fl):
    pass

def handle_file(fl):
    
    def create_dir():
        root,_=os.path.splitext(fl.filename)
        if root.endswith(".tar"):
            root=root[:-4]
        try:
            os.mkdir(PATH+root)
        except OSError :
            pass
        return root,PATH+root
    
    def unzip(dr,flnm):
        from zipfile import ZipFile
        with ZipFile(StringIO(fl.file.read())) as f:
            #f.testzip()
            f.extractall(dr)

    def untar(dr,flnm):
        from gzip import GzipFile
        from tarfile import TarFile
        cont=fl.file.read()
        flcont=StringIO(cont)
        try:
            f_ar=TarFile(fileobj=flcont)
            with  f_ar as f:
                f.extractall(dr)
        except tarfile.ReadError:
            #savepath="{0}/{1}".format(dr,fl.filename)
            f_gz=GzipFile(fileobj=StringIO(cont))
            f_tar=TarFile(fileobj=StringIO(f_gz.read()))
            with f_tar as f:
                f.extractall(dr)
            #print(START % savepath+"|||"+cont)
        return None

    try:
        flnm = os.path.basename(fl.filename)
        nm,dr=create_dir()
        if flnm.endswith((".tar.bz2",".tar.gzip",".tar",".gz",".tar.gz")):
            untar(dr,nm)
        elif flnm.endswith(".zip"):
            unzip(dr,nm)
        elif flnm.endswith((".tar.bz2",)):
            print(FAIL)
            return None
        else:
            with open("{0}/{1}".format(dr,flnm), "wb") as f:
                f.write(fl.file.read())
        print(SUCC)
    except AttributeError:
        render("None %s" % (fl.filename), form={})

def render(warnings="Nothing", form=None):
    
    form = cgi.FieldStorage() #if form is None else form
    try:
        fl = form["upfile"]
        if fl.filename:
            handle_file(fl)
        else:
            print(START % warnings)
    except KeyError:
        print(START % warnings)
        return None
        
        


if __name__ == '__main__':
    import cgitb; cgitb.enable(display=True)
    render()
