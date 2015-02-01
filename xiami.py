# -*- coding: cp936 -*-
import urllib
import urllib2
import cookielib
import re

#change your information
username = ''
password = ''

def login():
    login_url = 'http://www.xiami.com/web/login'
    data = {
        # change your information here
        'email' : username ,
        'password' : password ,
        'LoginButton' : '登 录'
        }
    login_data = urllib.urlencode(data)
    login_headers = {
        'Referer' : 'http://www.xiami.com/web/login' ,
        'User-Agent' : 'Mozilla/5.0'
        }

    #set cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)

    print 'Start Login...'
    req = urllib2.Request(login_url, data=login_data, headers=login_headers)
    response = urllib2.urlopen(req).read().decode('utf-8')

    match = re.search(u'我的近况', response)
    if match != None:
        #login success
        print 'Login Success!'       
        return True
    else:
        print 'Login Failed. Check your email and password.'
        return False

def signin(response):
    match = re.findall(ur'<a class="check_in" href="/web/checkin/id/(\d+)">每日签到</a>',\
                       response, re.S)[0]
    url = 'http://www.xiami.com/web/checkin/id/'+match
    headers = {
        'Referer' : 'http://www.xiami.com/web' ,
        'User-Agent' : 'Mozilla/5.0',
        }
    data = {}
    req = urllib2.Request(url, None , headers=headers)
    result = urllib2.urlopen(req).read().decode('utf-8')

    match = re.findall(ur'已连续签到(\d+)天', result, re.S)[0]
    if match:
        print 'Success! You have signed in %s days[Now]' %match
    else:
        print 'SignIn Failed. The evil-coder changed something.'
    
def checkin():
    checkin_url = 'http://www.xiami.com/web'
    headers = {
        'Referer' : 'http://www.xiami.com/profile',
        'User-Agent' : 'Mozilla/5.0'
        }
    creq = urllib2.Request(checkin_url, None , headers=headers)
    response = urllib2.urlopen(creq).read().decode('utf-8')

    #start to sign in
    match = re.findall(ur'<d.*?>已连续签到(\d+)天</div>',response, re.S)[0]

    if match:
        print 'Success! You have signed in %s days[already]' % match
    else:
        sighin(response)


if __name__ == '__main__':
    if login():
        checkin()
