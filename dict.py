#!/usr/bin/python
#coding=utf-8

import urllib2
import sys
import re
import bs4

def main():
    if len(sys.argv) == 2:
        word = sys.argv[1]
        # if non en?
        try:
            if re.findall('\w*',word)[0] == word:
                isen = True
            else:
                isen = False
            xmls = urllib2.urlopen('http://dict.cn/' + word).read()

            if isen == True:
                rem = re.compile(r'<li><span>(?P<test>.*?)</strong></li>')
                for i in rem.findall(xmls):
                    print i.replace('</span><strong>','')
            else:
                bs = bs4.BeautifulSoup(xmls)
                foo = str(bs.findAll(attrs={'class':'layout cn'})[0])
                rem = re.compile(r'<li><a href=".*?">(?P<test>.*?)</a></li>')
                for j,i in enumerate(rem.findall(foo)):
                    print j+1,i
        except:
            print 'Not found.'

    else:
        help()

def help():
    print 'usage:%s [word]' % sys.argv[0]

if __name__ == '__main__':
    main()

