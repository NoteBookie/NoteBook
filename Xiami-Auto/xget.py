# -*- coding: cp936 -*-
import urllib2
import requests
import xmltodict
import sys
import os

username = ''
password = ''
req = requests.session()

def valid(filename):
    return filename.replace(':','').replace('*','').replace(' ','')

def decode(eloc):
    start = eloc.find('h')
    row = int(eloc[0:start])
    length = len(eloc[start:])
    col = length/row
    newloc = list(eloc[1:])
    rightRow = length % row
    result = ''
    for i in xrange(length):
        x = i % row
        y = i / row
        p = 0
        if x <= rightRow:
            p = x * (col + 1) + y
        else:
            p = rightRow * (col + 1) + (x - rightRow) * col + y
        result += newloc[p]
    return urllib2.unquote(result).replace('^','0')

def login():
    url = 'https://login.xiami.com/member/login'
    data = {
        'email':username,
        'password':password,
        'done': 'http://www.xiami.com/account',
        'submit': '登 录'
        }
    headers = {
        'user-agent': 'Mozilla/5.0',
        }
    req.post(url, data=data, headers=headers)

def download(id, filename='MySongs'):
    response = req.get('http://www.xiami.com/song/playlist/id/%s' % id,
                       headers = {'user-agent': 'Mozilla/5.0',}).text
    data = xmltodict.parse(response)['playlist']['trackList']['track']
    name = data['title']
    #print name
    url = decode(data['location']).encode('utf-8')
    #print url
    if not os.path.exists(filename):
        print 'Creating a new folder...'
        os.mkdir(filename)    
    print 'Downloading: %s' % name

    if os.path.exists('%s\%s.mp3' % (filename, valid(name))):
        dflag = raw_input('This file is already existed, delete?(Y/N)')
        if dflag == 'y' :
            os.remove('%s\%s.mp3' % (filename, valid(name)))
            print '%s.mp3 [removed]' % name
        else:
            print '%s.mp3 [skipped]' % name
            
    command = 'curl -o ' + '%s\%s.mp3 '%(filename, valid(name)) + url
    command = command.encode('cp936')
    
    os.system(command)
    print '%s.mp3 [downloaded]' % name

if __name__ == '__main__':
    login()
    download('1769598794') #明年今日（Live）
    raw_input()
