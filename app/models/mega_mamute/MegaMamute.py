import scrapy
import json

class SpiderMegaMamute (scrapy.Spider):
	nome = 'SpiderMegaMamute'
	start_urls = ['http://www.megamamute.com.br/informatica/notebook?PS=16']

	download_delay = 1.5

def parse(self, response):
	for vitrine in response.css('div.x-product'):
		link_data = {
			'link': vitrine.css ('a::attr("href")').extract_first(),
			'name': vitrine.css ('a::attr("title")').extract_first()
		}

		yield link_data

	link_next = response.css('li li.next').extract_first()
	
	if link_next
		yield scrapy.Request(link_next)