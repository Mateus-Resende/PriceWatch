# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re

def first(sel, xpath):
    return sel.xpath(xpath).extract_first()

f = open('invalid_links.json', 'wb')
class SpiderIbyteComputadores(scrapy.Spider):

  name = 'spider'
  start_urls = ['http://www.ibyte.com.br/computadores/notebooks-1.html']
  download_delay = 1.5

  def parse(self, response):
      for produtos in response.xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/ul/li/a[contains(@title, "Notebook") or (contains(@title, "Mac")) or contains(@title, "Ultra")]'):
          link= produtos.xpath('./@href').extract()
          name= produtos.xpath('./@title').extract()
          yield dict(link=link, name=name)

      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(bateria|suporte|break|carca|tampa|base|stadard.console)"

      # se a validação não passar, escreva no arquivo de erros
      #if re.search(notebook_validation, name, re.IGNORECASE):
       # f.write(json.dumps(link_data) + '\n')

      # ou então, libere para o output do scrapy
      #else:
       # yield link_data

      link_next = response.xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div/div[3]/ol/li[@class="arrow right"]/a/@href').extract_first()

      if link_next:
          yield scrapy.Request(link_next)
