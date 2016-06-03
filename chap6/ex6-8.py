'''
Created on May 20, 2014

@author: igor
'''
#import sqlite3
import sqlite3
from pprint import pprint


def parse_acr_files():
    import json
    with open("acrsl.json") as f:
        acrs=json.load(f)
    return acrs


def zip_acrls(k,val):
    words,freqs=zip(*val)
    return k,",".join(words),",".join(freqs)



def to_html(args):
    html=u"<tr>{tds}</tr>".format(tds="".join(map(lambda x: u"<td>{}</td>".format(x),args)))
    print(html)
    return html


def main():
    with sqlite3.connect(':memory:') as c:
        conn=c.cursor()
        conn.execute('''CREATE TABLE acronyms (graphems , words, freq)''')
        conn.executemany("INSERT INTO acronyms VALUES (?,?,?)",[zip_acrls(k, val) for k,val in parse_acr_files().items()])
        conn.execute("SELECT * FROM acronyms ")
        html=u"<table>{}</table>".format("".join(map(to_html,conn.fetchmany(30))))
        with open("acr.html","wr") as f:
            html_wrap=uW"<html><head><meta charset='utf-8'></head>{html}</html".format(html=html)
            f.write(html_wrap.encode("utf8"))

main()