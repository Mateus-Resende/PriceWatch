import scrapy
import json

class SpiderFnac (scrapy.Spider):
	nome = 'spiderFnac'
	start_urls = ['http://www.fnac.com.br/informatica/notebook/8427']
	
	download_delay = 1.5

def parse(self, response):
	for vitrine in response.css('div.item'):
		link_data = {
			'link': vitrine.css ('a::attr("href")').extract_first(),
			'name': vitrine.css ('a::attr("title")').extract_first()
		}

		yield link_data

	link_next = response.css('div a.next.lnkPaginacao::attr("href")').extract_first()
	
	if link_next
		yield scrapy.Request(link_next)