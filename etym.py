#!/usr/bin/python
#coding=utf-8

import urllib2
import sys,os
from bs4 import BeautifulSoup
import re
import time

def match(s):
	r = re.compile('from ([\w\s-]+?)(\([\w\s-]+\))*? "(.*?)"',re.S | re.M)
	r2 = re.compile('\+ (\w+) "(.*?)"',re.S | re.M)

	l = []

	ret = r.findall(s)
	for word, foo, mean in ret:
		if word.count('from') > 1:
			word = word.split('from')[-1]
		word = word.strip().split(' ')[-1]
		l.append((word, mean))

	ret = r2.findall(s)
	for word, mean in ret:
		l.append((word, mean))
	
	with open('/home/latyas/test_etym.log','a') as f:
		for i in l:
			ss = '%s || %s\n' % i
			f.write(ss)
			print ss

def process_text(text):
    r = re.compile('<a.*?>(.*?)</a>')
    return r.sub("\\x1b[32;40;1m\\1\\x1b[0m",text)

def etymology(key):
    page = urllib2.urlopen("http://www.etymonline.com/index.php?term=" + key).read().decode("utf-8")
    if 'No matching terms found.' in page:
        return None
    soup = BeautifulSoup(page)
    foo = soup.findAll('div', id='dictionary')
    foo = foo[0].findAll('dd')
    foo = '\n'.join([''.join(map(str,bar.contents)) for bar in foo])
    match(BeautifulSoup(foo).text)
    foo = process_text(foo)
    foo = BeautifulSoup(foo).text
    foo = foo.replace(r'\x1b','\x1b')
    return foo
    return None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s [WORD]' % sys.argv[0]
        sys.exit(1)
    foo = etymology(sys.argv[1])
    if foo:
        print foo
    else:
        print 'Not Found'
