#!/usr/bin/python
#coding=utf-8

import urllib2
import sys
from bs4 import BeautifulSoup
import re 

def etymology(key):
	page = urllib2.urlopen("http://www.etymonline.com/index.php?term=" + key).read().decode("utf-8")
	if 'No matching terms found.' in page:
		return None
	try:
		soup = BeautifulSoup(page)
		foo = soup.findAll('div', id='dictionary')
		rep = re.compile('<img.*"/>?')
		ret = rep.sub('',str(foo[0]))
		ret = ret.replace('</div>','')
		ret = ret.replace('<div id="dictionary">','')
		
		return ret
	except:
		pass
	return None

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: %s [WORD]' % sys.argv[0]
		sys.exit(1)
	foo = etymology(sys.argv[1])
	if foo:
		foo = re.sub('<a .*?>.*?</a>','',foo)
		foo = re.sub('<(dt|dl|dd|span).*?>','',foo)
		foo = re.sub('</(dt|dl|dd|span)>','',foo)

		foo = foo.replace('\n\n','')
		foo += '\n'
		print foo
	else:
		print 'Not Found'
