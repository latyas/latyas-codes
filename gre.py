#!/usr/bin/python
#coding=utf-8

import urllib2
import re
import sys
from bs4 import BeautifulSoup

def get_context(key):
    ret = urllib2.urlopen('http://www.merriam-webster.com/dictionary/%s' % key).read().decode("utf-8")
    soup = BeautifulSoup(ret)
    foo = soup.findAll(attrs={"class":"scnt"})
    return str(foo)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s [WORD]' % sys.argv[0]
        sys.exit(1)

    keyword = sys.argv[1]
    data = get_context(keyword)
    bs = BeautifulSoup(data)
    foo = bs.findAll(attrs={'class':'scnt'})
    for j,i in enumerate(foo):
        i = str(i)
        i = re.subn('<(div|span|strong|em|a).*?>','',i)[0]
        i = re.subn('<sup.*?>.*?</sup>','',i)[0]
        i = i.replace(r'&lt;','')
        i = i.replace(r'&gt','')
        i = re.sub(r'</(strong|span|em|div|a)>','',i)
        i = i.replace('Â','')
        i = ' ' + i
        i = i.replace(r'  ','')
        i = i.replace(r'  ','')
        print '[%d] %s' % (j+1,i)
