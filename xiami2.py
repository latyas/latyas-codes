# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:33:08 2013

@author: latyas
"""

import xmltodict
import requests 
import sys
import urllib2
import os
from BeautifulSoup import BeautifulSoup
import json

def text_validate(text):
    return text.replace('\'','').replace('\\','').replace('/','')
def set_320k(s):
    url = 'http://www.xiami.com/vip/myvip'
    header = {'user-agent':'Mozilla/5.0'}
    ret = s.get(url,headers=header).text
    bs = BeautifulSoup(ret)
    user_id = bs.find('input',attrs={'id':'user_id'}).get('value')
    data = {'user_id':user_id,
            'tone_type':'1',
            '_xiamitoken':s.cookies.get('_xiamitoken')
            }
    ret = s.post('http://www.xiami.com/vip/update-tone',data=data,headers=header)
    ret = json.loads(ret.text)
    if ret['info'] == 'success':
        print 'Quality of the songs has set to 320kbps.'
    else:
        print 'You are not a VIP, songs will be downloaded as normal quality.'
 
def xiami(s):
    start = s.find('h')
    row = int(s[0:start])
    length = len(s[start:])
    column = length / row
    output = ''
    real_s = list(s[1:])
    
    sucks = []
    suck = length % row # = 0 -> good! if not , sucks!
    for i in range(1,suck+1):
        sucks.append(real_s[i*(column)])
        real_s[i*(column)] = 'sucks'
        real_s.remove('sucks')
    for i in range(column):
        output += ''.join(real_s[i:][slice(0,length,column)])
    output += ''.join(sucks)
    return urllib2.unquote(output).replace('^','0')

if len(sys.argv) < 3:
    print 'Usage:%s ALBUM_ID TYPE\n\talbum type:1 \t user-list type:3' % (sys.argv[0])
    sys.exit(0)
reload(sys)
sys.setdefaultencoding('utf-8')


username = 'test@yopmail.com'
password = '19920330'
axel_opts = '-n5'
login_url = 'https://login.xiami.com/member/login'
data = {'email':username,
        'password':password,
        'done':'http://www.xiami.com/account',
        'submit':'登 录'
}
header = {'user-agent':'Mozilla/5.0'}
hq = True #high quality? need VIP
album = sys.argv[1]
list_type = sys.argv[2]


req = requests.session()
ret = req.post(login_url,data=data,headers=header)
if hq: set_320k(req) # set quality to 320kbps
foo = req.get('http://www.xiami.com/song/playlist/id/%s/type/%s' % (album,list_type),headers={'user-agent':'Mozilla/5.0'}).text
data = xmltodict.parse(foo)['playlist']['trackList']['track']

delete_all = False

if len(sys.argv) == 4:
    if sys.argv[3] == '--overwrite':
        delete_all = True
        
for i in data:
    if not os.path.exists(text_validate(i['album_name'])):
        print 'Creating folder'
        os.system('mkdir \'%s\'' % text_validate(i['album_name']))
    if not os.path.exists('%s/cover.jpg' % (text_validate(i['album_name']))):
        print 'Downloading cover ...'
        os.system('curl \'%s\' > \'%s/cover.jpg\'' % (i['pic'].replace('_1',''), text_validate(i['album_name'])))
    file_name = text_validate(i['title']) + '.mp3'
    if not hq:
        url = xiami(i['location'])
    else:
        url = xiami(json.loads(req.get('http://www.xiami.com/song/gethqsong/sid/' + i['song_id'],headers=header).text)['location'])
    print 'Downloading',i['title']
    if os.path.exists('%s/%s.mp3' % (text_validate(i['album_name']),text_validate(i['title']))):
        if not delete_all:
            foofoo = raw_input('%s existed, delete?(for any key jumping, enter yes to delete, enter ALL (upper) to delete all existed)' % i['title'])
            if foofoo == 'yes':
                if foofoo == 'ALL':
                    delete_all = True
            else:
                print '********************** skipped *************************'
                continue
        os.system('rm \'%s/%s.mp3\'' % (text_validate(i['album_name']),text_validate(i['title'])))
    os.system('axel -n5 --user-agent="Mozilla/5.0" %s -o \'%s\'' % (url, '%s/%s' %(text_validate(i['album_name']),file_name)))
