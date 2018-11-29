# -*- coding: utf-8 -*-
import scrapy


class TinymixtapesSpider(scrapy.Spider):
	name = 'tinymixtapes'
	allowed_domains = ['tinymixtapes.com']
	start_urls = ['https://tinymixtapes.com/mix-tapes']

	def parse(self, response):
		urls = response.css('div.tile-panel__tiles > article.tile.tile--small-rect.tile--mix_tape > a::attr(href)').extract()
		for url in urls:
			url = response.urljoin(url)
			yield scrapy.Request(url=url, callback=self.parse_details)

		next_page_url = response.css('li.pager-next > a::attr(href)').extract_first()
		if next_page_url:
			next_page_url = response.urljoin(next_page_url)
			yield scrapy.Request(url=next_page_url, callback=self.parse)

	def parse_details(self, response):
		yield{
		'title' : response.css('header > h1 > span::text').extract(),
		'image_url' : response.css('div.entry__body > figure > img::attr(src)').extract(),
		'tracklist' : response.css('div.entry__body-text > p::text').extract(),
		'url' : response.url
		}
