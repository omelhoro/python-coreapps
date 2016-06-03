#!/usr/bin/env python
'''
Created on Jun 10, 2014

@author: igor
'''
import cgi
URL = '/cgi-bin/ex3.py'

HTML="""
<html>
<head><title>Feedback</title></head>
<body>%s
</body>
</html>"""
FORMBODY='''
<form action=%s
<p><label>Your email</label><input type=text name=email value=' '></p>
<p><label>Your comment</label><input type=text name=text size=60 value=' '></p>
<input type=submit>
</form>
''' % URL

THANK='<p>Thank you</p>'
ERROR_EM="<p>Not a valid email!</p>"
ERROR_CO="<p>No comment!</p>"

def save_data(*data):
    with open("ex3.com","a+") as f:
        f.write(",".join(data))

def process():
    form = cgi.FieldStorage()
    errors=''
    try:
        email,text=form["email"].value.strip(),form["text"].value.strip()
        if "@" not in email:
            errors+=ERROR_EM
        if not text:
            errors+=ERROR_CO
        if errors:
            print(HTML % errors+FORMBODY)
        else:
            save_data(email,text)
            print(HTML % THANK)
    except KeyError:
        print(HTML % FORMBODY)
    
if __name__ == '__main__':
    process()