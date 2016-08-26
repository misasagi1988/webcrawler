import os
import urllib
import urllib2
import cookielib
filename = "test.txt"
cookie = cookielib.MozillaCookieJar(filename)
httphandler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(httphandler)
response = opener.open("http://www.baidu.com")
cookie.save(ignore_discard=True, ignore_expires=True)
with open(filename) as pf:
    print pf.read()