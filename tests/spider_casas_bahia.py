# coding: utf-8
import scrapy

# RODE ESTE ARQUIO DA SEGUINTE FORMA :
# scrapy runspider spider_casas_banhia.py -o tabela_links.csv



class SpiderCasasBahia(scrapy.Spider):
    name = 'spider'
    start_urls = ['http://www.casasbahia.com.br/Informatica/Notebook/?Filtro=C56_C57']
    download_delay = 1.5

    def parse(self, response):
        for vitrine in response.css('.hproduct'):
            yield {
                #'Descrição': vitrine.css('strong::text').extract_first(),
		        'Descrição': vitrine.css('a::attr("title")').extract_first(),
                'link': vitrine.css('a::attr("href")').extract_first(),
            }
	link_next = response.css('li.next a::attr("href")').extract_first()
        if link_next:
            yield scrapy.Request(link_next)
