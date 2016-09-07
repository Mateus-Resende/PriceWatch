# coding: utf-8
import scrapy
import json
# biblioteca para expressões regulares no python
import re
import logging

f = open('invalid_links.json', 'wb')
class SpiderEletrosom(scrapy.Spider):

	name = 'spider'
	start_urls = ['http://www.novomundo.com.br/informatica-e-tablets/notebook']
	#download_delay = 1.5
	pag = 0

	def parse(self, response):
		for vitrine in response.css('li[class^="informatica-e-tablets--aparelhos-e-acessorios"]'):
			link_data = {
				"link": vitrine.css('a::attr("href")').extract_first(),
				"name": vitrine.css('a::attr("title")').extract_first()
			}

			# essa expressão regular (regex) retorna true se encontrar microcomputador OU ...
			notebook_validation = "(microcomputador|computador|impressora|tablet)"

			# se a validação não passar, escreva no arquivo de erros
			if re.search(notebook_validation, link_data['name'], re.IGNORECASE):
				f.write(json.dumps(link_data) + '\n')

			# ou então, libere para o output do scrapy
			else:
				yield link_data

		#pag_next = response.css('ul.pages').extract_first()
		#logging.info("----------- " + str(pag_next))
		self.pag += 1
		if self.pag < 5:
			link_next = "http://www.novomundo.com.br/buscapagina?fq=C%3a%2f1000050%2f1000155%2f&PS=24&sl=986d911b-16c5-43cb-b339-e890034ae514&cc=24&sm=0&PageNumber=" + str(self.pag)
			yield scrapy.Request(link_next)

			# curl 'http://www.novomundo.com.br/buscapagina?fq=C%3a%2f1000050%2f1000155%2f&PS=24&sl=986d911b-16c5-43cb-b339-e890034ae514&cc=24&sm=0&PageNumber=3'
			# curl 'http://www.novomundo.com.br/buscapagina?fq=C%3a%2f1000050%2f1000155%2f&PS=24&sl=986d911b-16c5-43cb-b339-e890034ae514&cc=24&sm=0&PageNumber=4'