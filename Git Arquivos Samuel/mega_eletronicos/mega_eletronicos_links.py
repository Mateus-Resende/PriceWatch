# coding: utf-8 
import scrapy

class SpiderCasasBahia(scrapy.Spider):
    name = 'spider'
    start_urls = [
        'http://www2.megaeletronicos.com/categoria-notebooks-166'
    ]
    download_delay = 1.5
    

    def parse(self, response):
        for vitrine in response.css('article.tall-lista-producto'):
            yield {
                'link' : vitrine.css('a::attr("href")').extract_first(),
            }

        for x in range(2, 5):
            link_next = response.css('.btn::attr("href")').extract()[x]
        
            if link_next:
                yield scrapy.Request(response.urljoin(link_next))

	