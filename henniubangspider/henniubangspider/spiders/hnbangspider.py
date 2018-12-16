# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy_splash import SplashRequest
from henniubangspider.items import HnbangspiderItem


class hnbangSpider(scrapy.Spider):
    name = 'hnbang'
    allowed_domains = ['http://hnbang.com']
    start_urls = ['http://hnbang.com/view/27458.html']

    def start_requests(self):
        url = 'http://hnbang.com/view/27458.html'
        requst = SplashRequest(url, callback=self.parse_one_page, dont_filter=True,
                                    args={'wait': 0.5, 'image_enable': False})
        requst.meta['url'] = url
        yield requst
        #yield self.spider_one_page(url)
        #yield scrapy.Request(url, callback=self.pareindexl)

    def parse_one_page(self, response):
        xpathPrePage = response.xpath('//span[@class="article-nav-prev"]/a/@href')
        preurl = xpathPrePage.extract()
        print preurl
        #self.getUsedInfo(response)
        #print "------------getUsedInfo-----------"
        pagename = ""
        baseurl = response.meta['url']
        regex_paggeindex = re.compile(r'http://hnbang.com/view/(\d+).html')
        pageindexls = regex_paggeindex.findall(baseurl)
        for pageindexl in pageindexls:
            pagename = pageindexl
        textlist = response.xpath('//article[@class="article-content"]/p/text()').extract()
        urllist = response.xpath('//article[@class="article-content"]/p/img/@src').extract()
        contextlist = []
        urlresultlist = []
        for text in textlist:
            #print len(text)
            if len(text) > 0:
                #print text
                contextlist.append(text)
        for url in urllist:
            #print len(url)
            if len(url) > 0 and url.endswith(".gif"):
                #print url
                urlresultlist.append(url)
        for indexl in range(0, min(len(contextlist), len(urlresultlist))):
            item = HnbangspiderItem()
            item["context"] = contextlist[indexl]
            item["gifurl"] = urlresultlist[indexl]
            item["pagename"] = pagename
            #print item
            yield item
        #preurl = xpathPrePage.xpath('//a/@href').extract()
        #print preurl
        for url in preurl:
            requst =  SplashRequest(url, callback=self.parse_one_page, dont_filter=True,
                                    args={'wait': 0.5, 'image_enable': False})
            requst.meta['url'] = url
            yield requst

    def getUsedInfo(self, response):
        #print "------------getUsedInfo-----------"
        pagename = ""
        baseurl = response.meta['url']
        regex_paggeindex = re.compile(r'http://hnbang.com/view/(\d+).html')
        pageindexls = regex_paggeindex.findall(baseurl)
        for pageindexl in pageindexls:
            pagename = pageindexl
        textlist = response.xpath('//article[@class="article-content"]/p/text()').extract()
        urllist = response.xpath('//article[@class="article-content"]/p/img/@src').extract()
        contextlist = []
        urlresultlist = []
        for text in textlist:
            print len(text)
            if  len(text) > 0:
                print text
                contextlist.append(text)
        for url in urllist:
            print len(url)
            if len(url) > 0 and url.endswith(".gif"):
                print url
                urlresultlist.append(url)
        items = []
        for indexl in range(0, min(len(contextlist),len(urlresultlist))):
            item = HnbangspiderItem()
            item["context"] = contextlist[indexl]
            item["gifurl"] = urlresultlist[indexl]
            item["pagename"] = pagename
            print item
            items.append(item)
        yield items
