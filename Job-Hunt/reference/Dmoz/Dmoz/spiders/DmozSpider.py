# -*- coding: utf-8 -*-
import scrapy
from Dmoz.items import DmozItem

class DmozspiderSpider(scrapy.Spider):
    name = "DmozSpider"
    allowed_domains = ["http://www.dmoz.org/"]
    start_urls = (
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    )

    # def parse(self, response):
    #     for href = response
    #     # for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
    #         url = response.urljoin(href.extract())
    #         yield scrapy.Request(url, callback=self.parse_dir_contents)

    # def parse_dir_contents(self, response):
    #     for sel in response.xpath('//ul/li'):
    #         item = DmozItem()
    #         item['title'] = sel.xpath('a/text()').extract()
    #         item['link'] = sel.xpath('a/@href').extract()
    #         item['desc'] = sel.xpath('text()').extract()
    #         yield item