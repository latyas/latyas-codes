#!/usr/bin/python
#coding=utf-8

try:
    import urllib2
except:
    import urllib.request as urllib2
import sys
import re
import os
import time
import json
try:
    from urllib import unquote
except:
    from urllib.parse import unquote

try:
    import bs4
except:
    print('BeautifulSoup4 wasn\'t installed')
    sys.exit(0)


def main():
    if len(sys.argv) == 2:
        word = sys.argv[1]
        # if non en?
        try:
            if re.findall('\w*', word)[0] == word:
                isen = True
            else:
                isen = False
            url = 'http://dict.cn/' + word.replace(' ', '%20')
            xmls = urllib2.urlopen(url).read()
            trans = ''
            if isen is True:
                rem = re.compile(r'<li><span>(?P<test>.*?)</strong></li>')
                for i in rem.findall(xmls):
                    print(i.replace('</span><strong>', ''))
                    trans += i.replace('</span><strong>', '') + ' | '
                bs = bs4.BeautifulSoup(xmls)
                foo = bs.findAll('div', attrs={'id': 'dict-chart-basic'})[0]
                jdata = json.loads(unquote(foo.get('data')))
                print('')
                for i in jdata.values():
                    print('%s:%s%% |' % (i['sense'], i['percent'])),
                print

            else:
                bs = bs4.BeautifulSoup(xmls)
                foo = str(bs.findAll(attrs={'class': 'layout cn'})[0])
                rem = re.compile(r'<li><a href=".*?">(?P<test>.*?)</a></li>')
                for j, i in enumerate(rem.findall(foo)):
                    print(j+1, i)
                    trans += i + ' | '
        except:
            print('%s Not found.' % sys.argv[1])
            return
        if trans == '':
            print('%s Not found.' % sys.argv[1])
            return
        #log

        date = '%d-%d-%d' % (time.localtime().tm_year, time.localtime().tm_mon,
                             time.localtime().tm_mday)
        try:
                f = open(os.path.expanduser("~/") + 'dict.log', 'a+')
                f.close()
        except:
                open(os.path.expanduser("~/") + 'dict.log', 'w').close()

        f = open(os.path.expanduser("~/") + 'dict.log', 'a+')
        if not date in f.read():
            f.writelines(date + '\n')
        f.writelines('[%s] %s\n' % (word, trans))
        f.close()

    else:
        help()


def help():
    print('usage:%s [word]' % sys.argv[0])

if __name__ == '__main__':
    main()
