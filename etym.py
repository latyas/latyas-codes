#!/usr/bin/python
#coding=utf-8

import urllib2
import sys,os
from bs4 import BeautifulSoup
import re
import time

def process_text(text):
    r = re.compile('<a.*?>(.*?)</a>')
    return r.sub("\\x1b[31;43;1m\\1\\x1b[0m",text)

def etymology(key):
    page = urllib2.urlopen("http://www.etymonline.com/index.php?term=" + key).read().decode("utf-8")
    if 'No matching terms found.' in page:
        return None
    soup = BeautifulSoup(page)
    foo = soup.findAll('div', id='dictionary')
    foo = foo[0].findAll('dd')
    foo = '\n'.join([''.join(map(str,bar.contents)) for bar in foo])
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
