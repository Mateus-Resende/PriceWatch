# -*- coding: utf-8 -*-
import re
from lxml import html
from helpers.http_client import HttpClient
from helpers.processors import Processors
from helpers.brands import Brands
from helpers.memory import Memory

class DataExtractor():

	def __init__(self, response, url):
		self.response = response
		self.url = url
		self.processors = Processors();
		self.brands = Brands();
		self.memory = Memory();

	def parse(self):
		namespaces = {'re': "http://exslt.org/regular-expressions"}
		data = {}
		data["store"] = "eletro_shopping"
		data["name"] = self.response.xpath('//div[@itemprop="name"]/h1//text()')
		data["name"] = self.validate_field(data, 'name')
		data["url"] = self.url
		data["price"] = self.response.xpath('//span[@itemprop="lowPrice"]//text()')
		data["price"] = self.normalize_price(data["price"])
		data["available"] = data["price"] != None and data["price"] != 0.0
		data["processor"] = self.response.xpath('//td[text()="Processador - Modelo"]/following-sibling::td//text()')
		data["processor"] = self.normalize_processor(self.validate_field(data, "processor"))
		data["brand"] = self.normalize_brand(data["name"])
		data["ram_memory"] = self.response.xpath('//td[contains(text(), "Mem") and contains(text(), "Capacidade")]/following-sibling::td//text()', namespaces = {'re' : 'http://exslt.org/regular-expressions'})
		data["ram_memory"] = self.normalize_memory(self.validate_field(data, "ram_memory"))
		data["sku"] = self.response.xpath('//div[@itemprop="name"]/span//text()')
		if(len(data['sku']) > 0):
			data["sku"] = data["sku"][0].split(':')[1].strip()
		else:
			data['sku'] = ''
		data["disco"] = {}
		disco = self.response.xpath('//td[text()="HD - Tipo"]/following-sibling::td//text()', namespaces={'re': "http://exslt.org/regular-expressions"})
		hd = ''
		ssd = ''
		if(len(disco) > 0):
			disco = disco[0]
			if(re.search('HD', disco, re.IGNORECASE) != None and re.search('SSD', disco, re.IGNORECASE) != None):
				aux = self.response.xpath('//td[text()="HD - Capacidade"]/following-sibling::td//text()', namespaces={'re': "http://exslt.org/regular-expressions"})
				if(len(aux) > 0):
					aux = aux[0];
					if(re.search('\\+', aux) != None):
						hd = aux.split('+')[0]
						ssd = aux.split('+')[1]
					else:
						hd = disco.split('HD')[0].strip();
						ssd = disco.split(' ')
						ssd = ssd[ssd.index('SSD') - 1]
			elif(re.search('HD', disco, re.IGNORECASE) != None):
				hd = self.response.xpath('//td[text()="HD - Capacidade"]/following-sibling::td//text()', namespaces={'re': "http://exslt.org/regular-expressions"})
				ssd = ''
			elif(re.search('SSD', disco, re.IGNORECASE) != None):
				hd = ''
				ssd = self.response.xpath('//td[text()="HD - Capacidade"]/following-sibling::td//text()', namespaces={'re': "http://exslt.org/regular-expressions"})
		data['disco']['hd'] = hd
		data['disco']['ssd'] = ssd
		data["display_size"] = self.response.xpath('//td[text()="Tela - Tamanho"]/following-sibling::td//text()', namespaces={'re': "http://exslt.org/regular-expressions"})
		data["display_size"] = self.validate_field(data, "display_size")

		return data

	def validate_field(self, data, field):
		return (data[field][0].strip() if (len(data[field]) > 0) else "")

	# normalize storage

	def normalize_memory(self, raw_data):
		if (re.search('16', raw_data, re.IGNORECASE) != None):
			return self.memory.get_16GB()
		elif (re.search('14', raw_data, re.IGNORECASE) != None):
			return self.memory.get_14GB()
		elif (re.search('12', raw_data, re.IGNORECASE) != None):
			return self.memory.get_12GB()
		elif (re.search('10', raw_data, re.IGNORECASE) != None):
			return self.memory.get_10GB()
		elif (re.search('8', raw_data, re.IGNORECASE) != None):
			return self.memory.get_8GB()
		elif (re.search('6', raw_data, re.IGNORECASE) != None):
			return self.memory.get_6GB()
		elif (re.search('4', raw_data, re.IGNORECASE) != None):
			return self.memory.get_4GB()
		elif (re.search('2', raw_data, re.IGNORECASE) != None):
			return self.memory.get_2GB()
		elif (re.search('1', raw_data, re.IGNORECASE) != None):
			return self.memory.get_1GB()

	def normalize_price(self, raw_data):
		try:
			raw_data = raw_data[0].strip() if (len(raw_data) > 0) else ""
			raw_data = raw_data.replace(".", "").replace(",", ".")
			return float(raw_data)
		except ValueError:
			return 0.0

	def normalize_brand(self, raw_data):
		if (re.search("dell", raw_data, re.IGNORECASE) != None):
			return self.brands.get_dell()
		elif (re.search('asus', raw_data, re.IGNORECASE) != None):
			return self.brands.get_asus()
		elif (re.search('apple', raw_data, re.IGNORECASE) != None):
			return self.brands.get_apple()
		elif (re.search('acer', raw_data, re.IGNORECASE) != None):
			return self.brands.get_acer()
		elif (re.search('samsung', raw_data, re.IGNORECASE) != None):
			return self.brands.get_samsung()
		elif (re.search('positivo', raw_data, re.IGNORECASE) != None):
			return self.brands.get_positivo()
		elif (re.search('lenovo', raw_data, re.IGNORECASE) != None):
			return self.brands.get_lenovo()
		elif (re.search('lg', raw_data, re.IGNORECASE) != None):
			return self.brands.get_lg()

	def normalize_processor(self, raw_data):

		# remove erros de enconding (ex: \u84d2)
		raw_data = re.sub('\\\u\w\w\w\w', '', raw_data)

		if (re.search("i3", raw_data, re.IGNORECASE) != None):
			return self.processors.get_i3()
		elif (re.search("i5", raw_data, re.IGNORECASE) != None):
			return self.processors.get_i5()
		elif (re.search("i7", raw_data, re.IGNORECASE) != None):
			return self.processors.get_i7()
		elif (re.search("Pentium", raw_data, re.IGNORECASE) != None):
			return self.processors.get_pentium_quad()
		elif (re.search("byt|baytrail", raw_data, re.IGNORECASE) != None):
			return self.processors.get_baytrail()
		elif (re.search("amd.+dual core", raw_data, re.IGNORECASE) != None):
			return self.processors.get_amd_dual()
		elif (re.search("atom", raw_data, re.IGNORECASE) != None):
			return self.processors.get_atom()
		elif (re.search("Intel.+Core.+M", raw_data, re.IGNORECASE) != None):
			return self.processors.get_core_m()
		elif (re.search("Celeron", raw_data, re.IGNORECASE) != None):
			return self.processors.get_celeron()
		elif (re.search("arm", raw_data, re.IGNORECASE) != None):
			return self.processors.get_arm_a9()
		elif (re.search("samsung", raw_data, re.IGNORECASE) != None):
			return self.processors.get_samsung()
