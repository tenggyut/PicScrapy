# -*- coding: utf-8 -*-
from tutorial.items import JdPicture
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.log import log


class JdSpider(CrawlSpider):
    name = "jd_spider"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://www.jd.com"
    ]

    rules = (
        # Rule(LinkExtractor(allow=('http://channel\.jd\.com/.*\.html.*', ))),
        # Rule(LinkExtractor(allow=('http://list\.jd\.com/.*\.html.*', ))),
        Rule(LinkExtractor(allow=(
            'http://item\.jd\.com/.*\.html',
            'http://list\.jd\.com/.*\.html.*',
            'http://channel\.jd\.com/.*\.html.*')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if 'item' in response.url:
            catalog = []
            for clog in response.xpath('//div[@class="breadcrumb"]/span/a'):
                if len(clog.xpath('text()').extract()) > 0:
                    catalog.append(clog.xpath('text()').extract()[0].encode('utf-8'))
                else:
                    log.err(response.url)
            for img in response.xpath('//div[@class="spec-items"]/ul/li/img')[0:1]:
                pic = JdPicture()
                pic["image_urls"] = img.xpath('@src').extract()[0].encode('utf-8')
                pic["title"] = img.xpath('@alt').extract()[0].encode('utf-8')
                pic["catalog"] = catalog
                yield pic
        else:
            yield JdPicture()
