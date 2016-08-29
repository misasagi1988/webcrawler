# -*- coding:utf-8 -*-

import urllib2
import re
class Tool(object):
    pattern_img = re.compile('<img.*?>| {7}')
    pattern_addr = re.compile('<a.*?>|</a>')
    pattern_line = re.compile('<tr>|<div>|</div>|</p>')
    pattern_td = re.compile('<td>')
    pattern_para = re.compile('<p.*?>')
    pattern_br = re.compile('<br><br>|<br>')

    def replace(self, content):
        content = re.sub(self.pattern_img, '', content)
        content = re.sub(self.pattern_addr, '', content)
        content = re.sub(self.pattern_line, '\n', content)
        content = re.sub(self.pattern_td, '\t', content)
        content = re.sub(self.pattern_para, '\n  ', content)
        content = re.sub(self.pattern_br, '\n', content)
        return content.strip()


class BDTB(object):
    def __init__(self, baseurl, see_lz):
        self.baseurl = baseurl
        self.see_lz = "?see_lz=" + str(see_lz)
        self.tool = Tool()
        self.default_filename = 'bdtb.txt'
        self.floor = 1

    def deleteFile(self):
        with open(self.default_filename, 'w'):
            print 'clear default file content'

    def getPage(self, page_index):
        try:
            request = urllib2.Request(self.baseurl + self.see_lz + "&pn=" + str(page_index))
            content = urllib2.urlopen(request).read().decode("utf-8")
            return content
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None

    def getTitle(self, content):
        #content = self.getPage(1)
        reg = '<h3 class="core_title_txt.*?>(.*?)</h3>'
        pattern = re.compile(reg, re.S)
        match_res = re.search(pattern, content)
        if match_res:
            return match_res.group(1).strip()
        else:
            return None

    def getPageNum(self, content):
        #content = self.getPage(1)
        reg = '<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>'
        pattern = re.compile(reg, re.S)
        match_res = re.search(pattern, content)
        if match_res:
            return match_res.group(1).strip()
        else:
            return None

    def getContent(self, page_index):
        content = self.getPage(page_index)
        if content:
            reg = '<div id="post_content_.*?>(.*?)</div>'
            pattern = re.compile(reg, re.S)
            match_res = re.findall(pattern, content)
            cont_list = []
            for item in match_res:
                item = '\n' + self.tool.replace(item) + '\n'
                cont_list.append(item.encode('utf-8'))
            return cont_list
        else:
            return None

    def writeFile(self, content, filename = None):
        if filename is None:
            filename = self.default_filename
        if not content:
            return
        with open(filename, 'a+') as f:
            for item in content:
                floortag = '\n%d floor------------------------------------------------------------\n' %self.floor
                self.floor = self.floor + 1
                f.write(floortag)
                f.write(item)

    def run(self):
        self.deleteFile()
        page_index = self.getPage(1)
        page_title = self.getTitle(page_index)
        page_number = self.getPageNum(page_index)
        print 'page title is: ', page_title
        print 'page number is: ', page_number
        for i in range(1, int(page_number) + 1):
            print 'now crawling page %s: ' %int(i)
            self.writeFile(self.getContent(i))
        print 'crawling end, total floor count: ', self.floor - 1




bdtb = BDTB("http://tieba.baidu.com/p/3138733512", 1)
bdtb.run()
