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
    for vitrine in response.css('article.single-product.vitrine230'):#classe do produto
      link_data = {
          'link': vitrine.css('form::attr("action")').extract_first(),
          'name': vitrine.css('a::attr("title")').extract_first()
        }
        
      yield link_data

    link_next = response.css('li a.pure-button.next::attr("href")').extract_first()
    if link_next:
      yield scrapy.Request(link_next)

#Clase do produto
#<div class="top-area-product">
#Link do produto
#<a href="http://www.americanas.com.br/produto/125569401/notebook-positivo-stilo-xri3150-intel-dual-core-4gb-500gb-tela-led-14-linux-cinza-escuro&amp;review=1"
