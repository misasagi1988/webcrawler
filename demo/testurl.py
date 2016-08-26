import os
import urllib
import urllib2
import cookielib
filename = "test.txt"
cookie = cookielib.MozillaCookieJar(filename)
httphandler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(httphandler)
data = urllib.urlencode({"os_username":"bella_meng", "os_password":"Garcelan520"})
url = "https://jr.trendmicro.com:8443/login.jsp?os_destination=%2Fsecure%2FRapidBoard.jspa%3FrapidView%3D82%26view%3Dplanning%26selectedIssue%3DSAL-52%26epics%3Dvisible"

response = opener.open(url, data)
cookie.save(ignore_discard=True, ignore_expires=True)

url2 = "https://jr.trendmicro.com:8443/secure/RapidBoard.jspa?rapidView=158&view=planning&selectedIssue=SAN-1766"
result = opener.open(url2)
print result.read()