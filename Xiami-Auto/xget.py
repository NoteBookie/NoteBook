# -*- coding: utf-8 -*-
from optparse import OptionParser
import urllib2
import requests
import xmltodict
import sys
import os

req = requests.session()

def valid(filename):
    return filename.replace(':','').replace('*','').replace(u'・','').replace(' ','_').replace('&#039;','\'')

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

def download(id, filename='MySongs'):
    response = req.get('http://www.xiami.com/song/playlist/id/%s' % id,
                       headers = {'user-agent': 'Mozilla/5.0',}).text
    
    data = xmltodict.parse(response)['playlist']['trackList']['track']
    name = valid(data['title'])
    
    url = decode(data['location']).encode('utf-8')

    if not os.path.exists(filename):
        print 'Creating a new folder...'
        os.mkdir(filename)    

    print 'Downloading: %s' % valid(name)

    flag = True
    if os.path.exists('%s\%s.mp3' % (filename, name)):
        dflag = raw_input('This file is already existed, delete?(Y/N)')
        if dflag in ('y','Y') :
            os.remove('%s\%s.mp3' % (filename, name))
            print '%s.mp3 [removed]' % name
        else:
            print '%s.mp3 [skipped]' % name
            flag = False
            
    if flag:
        command = 'curl -o ' + '%s\%s.mp3 '%(filename, name) + url
        command = command.encode('cp936')
        #print command
        os.system(command)
        print '%s.mp3 [downloaded]' % valid(name)

def downList(id , type):
    response = req.get('http://www.xiami.com/song/playlist/id/%s/type/%s' % (id, type),
                       headers={'user-agent': 'Mozilla/5.0'}).text
    songlist = xmltodict.parse(response)
    filename = 'songlist_' + id
    

    for song in songlist['playlist']['trackList']['track']:
        if(song == 'title'):
            sid = songlist['playlist']['trackList']['track']['song_id']
            download(sid, filename)
            break
        sid = song['song_id']
        print sid
        download(sid, filename)


if __name__ == '__main__':
    usage = 'usage: %prog [options] id'
    parser = OptionParser(usage, version='%prog 1.0')
    parser.add_option('-s', '--single' ,dest = 'sid',
                      help = 'Download single song. Give the song\'s id.')
    parser.add_option('-a', '--album', dest = 'aid',
                      help = 'Down Album. need album\'s id')
    parser.add_option('-l', '--list', dest = 'lid',
                      help = 'Down user\'s list. need list id')
    (options, args) = parser.parse_args()

    if options.sid:
        download(options.sid)
    elif options.aid:
        downList(options.aid,'1')
    elif options.lid:
        downList(options.lid,'3')
    else:
        parser.error('You can type -h to get help information.')

    #raw_input('[Press ENTER to exit]')
