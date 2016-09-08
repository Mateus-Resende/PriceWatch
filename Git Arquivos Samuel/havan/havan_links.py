# coding: utf-8 
import scrapy

class SpiderCasasBahia(scrapy.Spider):
    name = 'spider'
    start_urls = [
        'http://www.havan.com.br/informatica/notebook-e-ultrabooks'
    ]
    download_delay = 1.5
    

    def parse(self, response):
        for vitrine in response.css('.shelf-qd-v1-product-name'):
            yield {
                'link' : vitrine.css('a::attr("href")').extract_first(),
            }

	