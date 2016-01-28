# -*- coding: utf-8 -*-
import scrapy
from sjtubbs.items import SjtubbsItem


class CsboardSpider(scrapy.Spider):
	name = "csboard"
	url_base = "https://bbs.sjtu.edu.cn/"
	# allowed_domains = ["https://bbs.sjtu.edu.cn/"]
	start_urls = (
		'https://bbs.sjtu.edu.cn/bbsdoc?board=CS',
	)

	def parse(self, response):
		for sel in response.xpath('//tr'):
			item = SjtubbsItem()
			id_and_date = sel.xpath('td/text()').extract()
			author_and_title = sel.xpath('td/a/text()').extract()
			url = sel.xpath('td/a[contains(@href, "bbscon")]/@href').extract()
			if len(id_and_date) == 5 and len(author_and_title) == 2:
				item['title'] = author_and_title[1]
				item['id'] = id_and_date[0]
				item['date'] = id_and_date[2]
				item['url'] = self.url_base + url[0]
				request = scrapy.Request(item['url'], callback=self.parse_dir_contents)
				request.meta['item'] = item
				yield request

	def parse_dir_contents(self, response):
		item = response.meta['item']
		text = response.xpath('//pre/text()').extract()
		item['text'] = text[1]
		# print text[1]
		yield item