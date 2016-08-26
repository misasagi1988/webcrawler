# -*- coding:utf-8 -*-
import os
import urllib2
import re
import time

class QSBK(object):
    def __init__(self):
        self.enable = False
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        self.header = {"User-Agent": self.user_agent}
        self.page_index = 1
        self.url = "http://www.qiushibaike.com/hot/page/"
        self.stories = []

    def getPageContent(self, page_index):
        try:
            request = urllib2.Request(self.url + str(page_index), headers = self.header)
            response = urllib2.urlopen(request)
            return response.read().decode("utf-8")
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None

    def getPageStories(self, page_index):
        page_content = self.getPageContent(page_index)
        page_stories = []
        if page_content:
            reg = '<div.*?author clearfix">.*?<a.*?<img.*?>.*?<a href.*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div.*?content">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>'
            pattern = re.compile(reg, re.S)
            match_res = re.findall(pattern, page_content)
            if match_res:
                for item in match_res:
                    if re.search("img", item[2]) is None:
                        text = re.sub("<br/>", "\n", item[1])
                        page_stories.append([item[0].strip(), text.strip(), item[3].strip(),])
        return page_stories

    def loadPage(self):
        if self.enable:
            if len(self.stories) < 2:
                page_stories = self.getPageStories(self.page_index)
                if page_stories:
                    self.stories.append(page_stories)
                    self.page_index = self.page_index + 1

    def showStories(self, page_story, page_index):
        for story in page_story:
            arg = raw_input()
            if arg == "q":
                self.enable = False
                return
            self.loadPage()
            str_format = "now showing page: %s\nauthor: %s\ncontent: %s\nvote: %s" %(str(page_index), story[0], story[1], story[2])
            print str_format

    def run(self):
        self.enable = True
        self.loadPage()
        now_page = 1
        while True:
            if not self.enable:
                break
            if len(self.stories) >= 1:
                self.showStories(self.stories[0], now_page)
                del self.stories[0]
                now_page = now_page + 1

qsbk = QSBK()
qsbk.run()






