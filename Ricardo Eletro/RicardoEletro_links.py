# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re

f = open('invalid_links.json', 'wb')
class SpiderRicardoEletro(scrapy.Spider):

  name = 'spider'
  start_urls = ['http://www.ricardoeletro.com.br/Busca/Resultado/?loja=&q=notebook']
  download_delay = 1.5

  def parse(self, response):
    for vitrine in response.css('.nome-produto-vertical'):
      link_data = { 
          "link": vitrine.css('a::attr("href")').extract_first(),
          "name": vitrine.css('a::text').extract_first()
        }
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(bateria|suporte|break|carca|tampa|Mala|Maleta|base|stadard.console)"

      # se a validação não passar, escreva no arquivo de erros
      if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
        f.write(json.dumps(link_data) + '\n')

      # ou então, libere para o output do scrapy
      else:
        yield link_data

    link_next = response.xpath('').extract_first()
    if link_next:
      yield scrapy.Request(link_next)