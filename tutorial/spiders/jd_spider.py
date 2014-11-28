# -*- coding: utf-8 -*-
from tutorial.items import JdPicture
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class JdSpider(CrawlSpider):
    name = "jd_spider"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://www.jd.com"
    ]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('item\.jd\.com/.*\.html', )), callback='parse_item'),
        Rule(LinkExtractor(allow=('list\.jd\.com/.*\.html', )), callback='parse_item'),
    )

    def parse_item(self, response):
        catalog = []
        for clog in response.xpath('//div[@class="breadcrumb"]/span/a'):
            catalog.append(clog.xpath('text()').extract()[0].encode('utf-8'))
        for img in response.xpath('//div[@class="spec-items"]/ul/li/img'):
            pic = JdPicture()
            pic["image_urls"] = img.xpath('@src').extract()[0].encode('utf-8')
            pic["title"] = img.xpath('@alt').extract()[0].encode('utf-8')
            pic["catalog"] = catalog
            yield pic