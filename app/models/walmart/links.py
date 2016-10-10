# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re

f = open('invalid_links.json', 'wb')


class SpiderCasasBahia(scrapy.Spider):

    name = 'spider'
    start_urls = ['https://www.walmart.com.br/categoria/informatica/notebooks-e-ultrabooks/?fq=C:4699/4701/&PS=20']
    download_delay = 1.5

    def parse(self, response):
        for vitrine in response.css('.shelf-product-item'):
            link_data = {
                "link": vitrine.css('a::attr("href")').extract_first(),
                "name": vitrine.css('a::attr("title")').extract_first()
            }

            # essa expressão regular (regex) retorna true se encontrar o texto entre parentesis...
            notebook_validation = "(memória para)"

            # se a validação passar, libere para o output do scrapy
            if !re.search(notebook_validation, link_data['name'], re.IGNORECASE):
                yield link_data

            # ou então, escreva no arquivo de erros
            else:
                f.write(json.dumps(link_data) + '\n')
