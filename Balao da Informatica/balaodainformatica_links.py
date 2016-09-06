# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re

f = open('invalid_links.json', 'wb')
class SpiderBalaoDaInformatica(scrapy.Spider):

  name = 'spider'
  start_urls = ['http://www.balaodainformatica.com.br/produtos/informatica/notebook-e-ultrabook']
  download_delay = 1.5

  def parse(self, response):
    for conteudo_produtos in response.css('.produtos-box'):
      link_data = { 
          "link": conteudo_produtos.css('a::attr("href")').extract_first(),
          "name": conteudo_produtos.css('b::text').extract_first()
        }
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(bateria|suporte|break|carca|tampa|Mala|Maleta|base|stadard.console)"

      # se a validação não passar, escreva no arquivo de erros
      if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
        f.write(json.dumps(link_data) + '\n')

      # ou então, libere para o output do scrapy
      else:
        yield link_data

    link_next = response.css('li.next a::attr("href")').extract_first()
    if link_next:
      yield scrapy.Request(link_next)