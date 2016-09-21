# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re

#variavel de controle
cont = 0

f = open('invalid_links.json', 'wb')
class SpiderLojasAmericanas(scrapy.Spider):

  name = 'spider'
  download_delay = 1.5
  start_urls = ['http://www.submarino.com.br/linha/271288/informatica/notebook?ofertas.limit=90']
  
  global cont
  
  
  def parse(self, response):
  
    for vitrine in response.xpath("//*[@id='vitrine']/article"):#classe do produto
      
      link = vitrine.xpath("./div[@itemprop='item']/form/div/a/@href").extract_first()
      name = vitrine.xpath("./div[@itemprop='item']/form/div/a/@title").extract_first()
      
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(Notebook|Ultrabook|Lenovo|Asus|Tela|Apple|Probook|Intel)"
      
      # se a validação não passar, escreva no arquivo de erros
      if re.search(notebook_validation, name, re.IGNORECASE):
        yield dict(link=link, name=name)
      
      # ou então, libere para o output do scrapy
      else:
        f.write(json.dumps(link) + json.dumps(name) + '\n')
      
      
    #avanço de pagica
    #O site não possui botão proximo
    #O site avança as paginas com uma progração constante na url
    global cont
      #chamada de funccao global
    cont += 90
    link = 'http://www.submarino.com.br/linha/271288/informatica/notebook?ofertas.limit=90&ofertas.offset='
    next = link+str(cont)
      
    #Criterio de parada: não encontrar mais vitrines
    if response.xpath("//*[@id='vitrine']/article"):
      yield scrapy.Request(next)
