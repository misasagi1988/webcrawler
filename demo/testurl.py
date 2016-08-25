import os
import urllib
import urllib2
values = {}
values["username"] = "meng_yujing@yeah.net"
values["password"] = "Misasagi1988"
data = urllib.urlencode(values)
url = "http://passport.csdn.net/account/login"
geturl = url + "?" + data
print geturl
#request = urllib2.Request("http://www.baidu.com")
#response = urllib2.urlopen(request)
#print response.read()