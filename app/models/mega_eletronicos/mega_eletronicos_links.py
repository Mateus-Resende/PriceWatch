
# coding: utf-8
import scrapy
import json
import re

f = open('invalid_links.json', 'wb')

class LinksExtractor(scrapy.Spider):

  name = 'spider'
  start_urls = ['http://www2.megaeletronicos.com/categoria-notebooks-166']
  download_delay = 1.5

  def parse(self, response):
    for vitrine in response.css('article.tall-lista-producto'):
      link_data = { 
          "link": vitrine.css('a::attr("href")').extract_first(),
	        "name": vitrine.css('.titulo-c::text').extract_first()
        }
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(bateria|smartphone|Chromebook|suporte|break|carca|tampa|base|stadard.console)"

      # se a validação não passar, escreva no arquivo de erros
      if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
        f.write(json.dumps(link_data) + '\n')

      # # ou então, libere para o output do scrapy
      else:
        yield link_data


    for x in range(2, 5):
        link_next = response.css('.btn::attr("href")').extract()[x]
    
        if link_next:
            yield scrapy.Request(response.urljoin(link_next))

	
