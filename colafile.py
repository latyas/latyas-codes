# colafile downloader

import re
import sys
import requests

s = requests.session()
ids = []
if len(sys.argv) < 2:
	# print usage
	print 'usage: %s [ID1] [ID2] ...' % sys.argv[0]
	sys.exit(0)
	
for id in sys.argv[1:]:
	ids.append(str(id))
for id in ids:
	try:
		data = {'action':'get_down',
			'file_id':id,
			'antiads':'0',
			't':'0'}
		header = {'Referer':'http://www.colafile.com/'}

		s.get('http://www.colafile.com/down/'+id)
		ret = s.get('http://www.colafile.com/ajax.php',params=data,headers=header)
		ret = re.findall('\+= \'(.*?)\';',ret.text)[0]
		
		if ret == '':
			raise Exception
			
		print 'http://d.colafile.com/'+ret
	except:
		print '[DEBUG] Exception arouse when processing %s' % id
