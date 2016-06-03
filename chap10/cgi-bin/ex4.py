#!/usr/bin/env python

'''
Created on Jun 10, 2014

@author: igor
'''
import cgi
from time import ctime
URL = '/cgi-bin/ex4.py'

HTML="""
<html>
<head><title>Guest Book</title></head>
<body>%s
</body>
</html>"""
FORMBODY='''
<p>Leave an entry:</p>
<form action=%s
<p><label>Your name</label><input type=text name=name value='' required=true></p>
<p><label>Your email</label><input type=text name=email value='' required=true></p>
<p><label>Your comment</label><input type=text name=text size=60 value='' required=true ></p>
<input type=submit>
</form>
<a href=%s >See all entries</a>
''' % (URL,URL+"?action=showents")

THANK='<p>Thank you</p>'
ERROR_EM="<p>Not a valid email!</p>"
ERROR_NM="<p>Not a valid name!</p>"
ERROR_CO="<p>Empty comment!</p>"
FLPT="ex4.com"

def save_data(*data):
    with open(FLPT,"a+") as f:
        f.write(",".join(data)+"\n")

def show_data():
    with open (FLPT,"rb") as f:
        csv=map( lambda x: x.strip().split(",")[1:] ,f.readlines())
    render_entry=lambda x: "<p>{user} said on {date}: {mes}</tr>".format(user=x[0].upper(),mes=x[1],date=x[2])
    tbody=map(render_entry,csv)
    print( HTML % ("".join(tbody)))

def process():
    form = cgi.FieldStorage()
    errors=''
    try:
        if form["action"].value=="showents":
            return show_data() 
    except KeyError:
        pass
    try:
        name,email,text=map(lambda x: x.value.strip(),[form["name"],form["email"],form["text"]])
        if "@" not in email:
            errors+=ERROR_EM
        if not text:
            errors+=ERROR_CO
        if not name:
            errors+=ERROR_NM

        if errors:
            print(HTML % errors+FORMBODY)
        else:
            save_data(email,name,text,ctime())
            print(HTML % THANK)
    except KeyError:
        print(HTML % FORMBODY)
    
if __name__ == '__main__':
    process()