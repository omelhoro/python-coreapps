#!/usr/bin/env python
'''
Created on Jun 9, 2014

@author: igor
'''

import cgi
from urllib import quote_plus

HEADER = 'Content-Type: text/html\n\n'
URL = '/cgi-bin/ex1_2.py'


ERRHTML = '''<HTML><HEAD><TITLE>
Friends CGI Demo</TITLE></HEAD>
<BODY><H3>ERROR</H3>
<B>%s</B><P>
<FORM><INPUT TYPE=button VALUE=Back
ONCLICK="window.history.back()"></FORM>
</BODY></HTML>'''

FORMHTML = '''<html>
<head>
<title>friends cgi demo</title>
<script type='text/javascript' src='/friendsCheck.js'></script>
</head>
<body><h3>friends list for: <i>%s</i></h3>
<form action="%s">
<b>enter your name:</b>
<input type=hidden name=action value=edit>
<input id='name' type=text name=person value="%s" size=15>
<p><b>how many friends do you have?</b>
%s
</form>
<p><button id='sbmt' onclick='check()'>Submit it</button>
<p id='inputErrors'></p>
</body>
</html>'''

RESTHTML = '''<HTML><HEAD><TITLE>
Friends CGI Demo</TITLE></HEAD>
<BODY><H3>Friends list for: <I>%s</I></H3>
Your name is: <B>%s</B><P>
You have <B>%s</B> friends.
<P>Click <A HREF="%s">here</A> to edit your data again.</p>
<P>Click <A HREF="%s">here</A> to look at the Dbase.</p>
</BODY></HTML>'''

TABLE='''<html>
<HEAD><TITLE>
Friends CGI Demo</TITLE></HEAD>
<body>
<H3>records</H3>
<table>
%s
</table>
</body>
<p>click <a href="%s">here</a> to clear the dbase.</p>
<input type=button value=back
onclick="window.history.back()">
</html>'''

FRADIO = '<INPUT TYPE=radio NAME=howmany VALUE="%s" %s> %s\n'
PATH="."
FLNM="friends.csv"
FLPT="{path}/{flnm}".format(path=PATH,flnm=FLNM)
def record_data(*data):
    with open(FLPT,"a") as f:
        f.write(",".join(data)+"\n")
    
def show_records():
    with open (FLPT,"rb") as f:
        csv=map( lambda x: x.strip().split(",") ,f.readlines())
    render_tds=lambda x: "<td>{}</td>".format(x)
    render_trs=lambda x: "<tr>{}</tr>".format("".join(x))
    tbody=map(render_trs,[map(render_tds,ln) for ln in csv])
    newurl_clearall = URL + '?action=clearall'
    print HEADER + TABLE % ("".join(tbody),newurl_clearall)
        
        

def clear_records(who, howmany):
    with open(FLPT,"w+") as f:
        f.write("")
    showForm(who, howmany)

def showError(error_str):
  print HEADER + ERRHTML % error_str


def showForm(who, howmany):
  friends = []
  for i in map(str, (0, 10, 25, 50, 100)):
      checked = ''
      if i == howmany:
          checked = 'CHECKED'
      friends.append(FRADIO % (i, checked, i))
  print '%s%s' % (HEADER, FORMHTML % (
      who, URL, who, ''.join(friends)))


def doResults(who, howmany):
      newurl = URL + '?action=reedit&person=%s&howmany=%s' % (quote_plus(who), howmany)
      newurl_showall = URL + '?action=showall'
      record_data(who,howmany)
      print HEADER + RESTHTML % (who, who, howmany, newurl,newurl_showall)

def process():
  error = ''
  form = cgi.FieldStorage()

  try:
      who = form['person'].value.title()
      if not who.strip():
          error+="You forgot the name.\n"
  except KeyError:
      who = 'NEW USER'

  try:
      howmany = form['howmany'].value
  except KeyError:
      if 'action' in form and form['action'].value == 'edit':
          error += 'Please select number of friends.'
      else:
          howmany = 0

  if not error:
    try:
        if form['action'].value == 'reedit':
              showForm(who, howmany)
        elif form['action'].value == 'showall':
              show_records()
        elif form['action'].value == 'clearall':
              clear_records(who, howmany)
        else:
              doResults(who, howmany)
    except KeyError:
        showForm(who, howmany)
  else:
      showError(error)

if __name__ == '__main__':
    process()
