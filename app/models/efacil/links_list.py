# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re

#f = open('invalid_links.json', 'wb')
class SpiderOnofreEletro(scrapy.Spider):

  name = 'spider'
  start_urls = ['http://www.efacil.com.br/loja/departamento/Informatica/Notebook/?loja=uberlandia']
  download_delay = 1.5

  
  def parse(self, response):
    for vitrine in response.css('.block-product'):
      link_data = { 
         "nome": vitrine.css('h3 a input::attr("value")').extract_first(),
         "link": vitrine.css('a::attr("href")').extract_first()
         #//*[@id="WC_CatalogEntryDBThumbnailDisplayJSPF_564007_link_9b"]/text()
        }
          
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      #notebook_validation = "(bateria|suporte|break|carca|tampa|base|stadard.console)"

      # se a validação não passar, escreva no arquivo de erros
      #if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
      #  f.write(json.dumps(link_data) + '\n')

      # ou então, libere para o output do scrapy
      #else:
      yield link_data

      link_next = response.css('a.right_arrow').extract_first()
      if link_next:
        yield scrapy.Request(link_next)