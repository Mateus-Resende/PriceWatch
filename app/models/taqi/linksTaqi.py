# coding: utf-8
import scrapy
import json
import re

f = open('invalid_links.json', 'wb')
class SpiderTaqi(scrapy.Spider):

#http://www.taqi.com.br/taqi/informatica/notebook/cat40004/
# LOJAS TAQI -- VANESSA

  name = 'spider'
  start_urls = ['http://www.taqi.com.br/taqi/informatica/notebook/cat40004','http://www.taqi.com.br/taqi/informatica/ultrabook/cat730006']
  download_delay = 1.5
  paginador = 0

  def parse(self, response):
    for vitrine in response.css('.container_produto.box_default_produtomaior'):
      link_data = { 
          "link": 'http://www.taqi.com.br'+ vitrine.css('div.foto_produto a::attr("href")').extract_first(),
          "name": vitrine.css('div.dados_default span.showTitleProducts::text').extract_first()
        }
      
      # essa expressão regular (regex) retorna true se encontrar bateria OU suporte OU break OU ...
      notebook_validation = "(bateria|suporte|break|carca|tampa|base|stadard.console)"

      # se a validação não passar, escreva no arquivo de erros
      if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
        f.write(json.dumps(link_data) + '\n')

      # ou então, libere para o output do scrapy
      else:
        yield link_data

    self.paginador += 1
    if self.paginador < 3:
      link_next = "http://www.taqi.com.br:80/browse/category.jsp?categoryId=cat40004&q_pageNum=" + str(self.paginador)
      yield scrapy.Request(link_next)     
        
    #http://www.taqi.com.br:80/browse/category.jsp?categoryId=cat40004&q_pageNum=2
    # PAGINADOR É UM SELECT. 
    