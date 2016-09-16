# coding: utf-8 
import scrapy
import csv

class SpiderCasasBahia(scrapy.Spider):
    name = 'spider'

    lista_link = []
    cr = csv.reader(open("tabela_links.csv","rb"))
    for row in cr: 
        lista_link.append(row[0])

    del lista_link[0]

    start_urls = lista_link

    download_delay = 1.5
    

    def parse(self, response):
        #for carac in response.css('.Processador'):
        yield {
            'description' : response.xpath('normalize-space(//*[@class="sTit"]/text())').extract_first(),
            'processador': response.xpath('normalize-space(//*[@class="Processador"]/dd/text())').extract_first(),
            'memory_cache': response.xpath('normalize-space(//*[@class="Cache even"]/dd/text())').extract_first(),
            'ram_memory': response.xpath('normalize-space(//*[@class="Memoria-RAM even"]/dd/text())').extract_first(),
            'hard_disc': response.xpath('normalize-space(//*[@class="Disco-rigido--HD-"]/dd/text())').extract_first(),
            'system': response.xpath('normalize-space(//*[@class="Sistema-operacional"]/dd/text())').extract_first(),
        }