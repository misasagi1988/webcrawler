import os
import urllib
import urllib2
import cookielib
cookie = cookielib.CookieJar()
httphandler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(httphandler)
response = opener.open("http://www.baidu.com")
for item in cookie:
    print "Name: ", item.name
    print "Value: ", item.value