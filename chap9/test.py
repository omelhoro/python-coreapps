'''
Created on Jun 7, 2014

@author: igor
'''
import subprocess as sb

text = 'hello'
proc = sb.Popen(
    './a.out',stdout=sb.PIPE,
    stdin=sb.PIPE)
proc.stdin.write(text)
proc.stdin.close()
result = proc.stdout.read()
print result
proc.wait()