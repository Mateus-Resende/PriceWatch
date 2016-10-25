# coding: utf-8
import scrapy
import json
import re

#variavel de controle para a contagem e avanço de página
cont = 0

#Arquivo de saida para os links invalidos
f = open('invalid_links.json', 'wb')

class LinksExtractor(scrapy.Spider):

  name = 'spider'
  start_urls = ['http://www.submarino.com.br/linha/271288/informatica/notebook?ofertas.limit=90/']
  download_delay = 1.5
  
  #inicio da funcao de spider
  def parse(self, response):
    #Procurando cada produto na exibição do site e para cada um, um ciclo do 'for'
    for vitrine in response.xpath("//*[@id='vitrine']/article"):
      #estrutura que armazena o nome e o link para um produto individual
      link_data = {
          "link": vitrine.xpath("./div[@itemprop='item']/form/div/a/@href").extract_first(),
          "name": vitrine.xpath("./div[@itemprop='item']/form/div/a/@title").extract_first()
        }
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(Notebook|Ultrabook|Cloudbook|Dell|Lenovo|Asus|Tela|Apple|Probook|Intel)"
      
      # se a validação passar, escreva no output do scrapy
      if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
        yield link_data
      
      # # ou então, escreva no arquivo de erros
      else:
        f.write(json.dumps(link_data) + '\n')
    
    
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
    
  
