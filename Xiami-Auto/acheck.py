# -*- coding: cp936 -*-
import re
import requests

s = requests.session()

def login():
    login_url = 'http://www.xiami.com/web/login'
    data = {
        # change your information here
        'email' : '' ,
        'password' : '' ,
        'LoginButton' : '登 录'
        }
    login_headers = {
        'Referer' : 'http://www.xiami.com/web/login' ,
        'User-Agent' : 'Mozilla/5.0'
        }
    print 'Start Login...'
    response = s.post(login_url, data=data, headers=login_headers).text

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
    result = s.get(url, headers = headers).text
    
    match = re.findall(ur'已连续签到(\d+)天', result, re.S)
    if match != []:
        print 'Success! You have signed in %s days[Now]' % match[0]
    else:
        print 'SignIn Failed. The evil-coder changed something.'
    
def checkin():
    checkin_url = 'http://www.xiami.com/web'
    headers = {
        'Referer' : 'http://www.xiami.com/profile',
        'User-Agent' : 'Mozilla/5.0'
        }
    response = s.get(checkin_url, headers = headers).text
    
    match = re.findall(ur'已连续签到(\d+)天', response, re.S)
    if match != []:
        print 'Success! You have signed in %s days[already]' % match[0]
    else:
        signin(response)


if __name__ == '__main__':
    if login():
        checkin()
