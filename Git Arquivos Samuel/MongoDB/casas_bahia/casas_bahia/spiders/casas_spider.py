from scrapy import Spider, Request

from scrapy.selector import Selector

from casas_bahia.items import CasasBahiaItem


class CasasSpider(Spider):
    name = "casas"
    allowed_domains = ["casasbahia.com.br"]
    start_urls = [
        "http://www.casasbahia.com.br/Informatica/Notebook/?Filtro=C56_C57",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="hproduct"]')

        for question in questions:
            item = CasasBahiaItem()
            item['title'] = question.xpath(
                'a[@class="link url"]/@title').extract()[0]
            item['url'] = question.xpath(
                'a[@class="link url"]/@href').extract()[0]
            yield item

	    link_next = response.css('li.next a::attr("href")').extract_first()
	    if link_next:
	    	yield Request(link_next)
