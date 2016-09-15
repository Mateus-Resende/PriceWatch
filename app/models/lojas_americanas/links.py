# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re

f = open('invalid_links.json', 'wb')
class SpiderLojasAmericanas(scrapy.Spider):

  name = 'spider'
  download_delay = 1.5
  start_urls = ['http://www.americanas.com.br/linha/267868/informatica/notebook']

  def parse(self, response):
    for vitrine in response.xpath("//*[@id='vitrine']/article"):#classe do produto
      link = vitrine.xpath("./div[@itemprop='item']/form/div/a/@href").extract_first()
      name = vitrine.xpath("./div[@itemprop='item']/form/div/a/@title").extract_first()
      
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(Notebook|Ultrabook|Lenovo|Asus|Tela|Mac|Netbook|Probook)"
      
      # se a validação não passar, escreva no arquivo de erros
      if re.search(notebook_validation, name, re.IGNORECASE):
        yield dict(link=link, name=name)
      
      # ou então, libere para o output do scrapy
      else:
        f.write(json.dumps(link) + json.dumps(name) + '\n')
      
      
    link_next = response.css('li a.pure-button.next::attr("href")').extract_first()
    if link_next:
      yield scrapy.Request(link_next)
