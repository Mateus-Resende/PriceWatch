#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from lxml import etree
from helpers.processors import Processors
from helpers.brands import Brands
from helpers.memory import Memory
from bs4 import BeautifulSoup


class DataExtractor:

    def __init__(self, response, url):
        self.response = response
        self.url = url
        self.processors = Processors()
        self.brands = Brands()
        self.memory = Memory()

    def parse(self):

        data = {}

        r = self.response
        
        # produtos da magazine luiza
        data['store'] = 'magazine_luiza'
		
		# nome do produto
        try:
        	data['name'] = r.find('h1', {'itemprop': 'name'})
        	data['name'] = self.validate_field(data, 'name')
        except (ValueError, TypeError, AttributeError):
        	data['name'] = ''
		
		# url como variavel global da classe
        data['url'] = self.url
				
		# preço do produto
        try:
        	data['price'] = r.findAll('meta', {'itemprop': 'price'})
        	data['price'] = self.normalize_price(data['price'])
        except (ValueError, TypeError, AttributeError):
        	data['price'] = 0.0
        
        # disponibilidade
        try:
        	data['available'] = self.set_available(r)
        except (ValueError, TypeError, AttributeError):
        	data['available'] = False
        
        try:
        	# processador
        	data['processor'] = r.find(text=re.compile(r'Processador')).parent.parent.find('div', {'class': 'fs-right'}).find(text=re.compile(r'Modelo')).parent.parent.find('p').text
        	data['processor'] = self.normalize_processor(data['processor'])
        except (ValueError, TypeError, AttributeError):
        	data['processor'] = ''
		           
        # marca
        try:
	        data['brand'] = r.find(text=re.compile(r'Marca')).parent.parent.find('p').text
        except (ValueError, TypeError, AttributeError):
        	data['brand'] = ''
		
		# memória ram
        try:
        	data['ram_memory'] = r.find('strong', text=re.compile(u'Memória')).parent.find('div', {'class':'row-fs-right'}).find('p').text
        except (ValueError, TypeError, AttributeError):
        	data['ram_memory'] = ''
		
		# sku para identificação
        try:
        	data['sku'] = r.find('div', {'data-product-id': True})['data-product-id']
        except (ValueError, TypeError, AttributeError):
        	data['sku'] = ''
        
        # armazenamento (SSD/HD)
        try:
        	hdd = r.find('strong', text=re.compile(r'HDD')).parent.find('div', {'class':'row-fs-right'}).findAll('p')
        	data['storage'] = self.normalize_storage(hdd[0].text, hdd[1].text)
        except (ValueError, TypeError, AttributeError):
        	data['storage'] = {}
        
        
        # tamanho da tela
        try:
        	data['display_size'] = r.find(text=re.compile(r'Polegadas')).parent.parent.find('p').text.strip(" \"").replace(",", ".") + "\""
        except (ValueError, TypeError, AttributeError):
        	data['display_size'] = ''
        
        #self.prints(data)
        
        return data

    def set_available(self, response):
        meta = response.find('meta', {'itemprop': 'availability'})
        if meta != None:
        	meta = meta['content'].strip()
        	if meta == 'InStock':
        		return True
        return False

    def validate_field(self, data, field):
    	if data[field] != None:
	    	return (data[field].get_text().strip() if (len(data[field]) > 0) else '')

    def normalize_storage(self, hd, ssd):
        result = {}
        
        if hd != None and len(hd) > 0:
        	result['HD'] = re.search('\d+.+[TG]B', hd)
        	if result['HD'] != None:
        		result['HD'] = result['HD'].group()    
		if ssd != None and len(ssd) > 0 and result == None:
			result['SSD'] = re.search('\d+.+[TG]B', ssd)
			if result['SSD'] != None:
				result['SSD'] = result['SSD'].group()

        return result

    def normalize_memory(self, raw_data):
        if re.search('16', raw_data, re.IGNORECASE) != None:
            return self.memory.get_16GB()
        elif re.search('12', raw_data, re.IGNORECASE) != None:
            return self.memory.get_12GB()
        elif re.search('14', raw_data, re.IGNORECASE) != None:
            return self.memory.get_14GB()
        elif re.search('10', raw_data, re.IGNORECASE) != None:
            return self.memory.get_10GB()
        elif re.search('8', raw_data, re.IGNORECASE) != None:
            return self.memory.get_8GB()
        elif re.search('6', raw_data, re.IGNORECASE) != None:
            return self.memory.get_6GB()
        elif re.search('4', raw_data, re.IGNORECASE) != None:
            return self.memory.get_4GB()
        elif re.search('2', raw_data, re.IGNORECASE) != None:
            return self.memory.get_2GB()
        elif re.search('1', raw_data, re.IGNORECASE) != None:
            return self.memory.get_1GB()
            
    def prints(self, data):
		print 'store: ' + data['store']
		print 'name: ' + data['name']
		print 'url: ' + data['url']
		print 'price: ' + str(data['price'])
		print 'available: ' + str(data['available'])
		print 'processor: ' + data['processor']
		print 'brand: ' + data['brand']
		print 'ram_memory: ' + data['ram_memory']
		print 'sku: ' + data['sku']
		print 'storage: ' + str(data['storage'])
		print 'display_size: ' + data['display_size']
		print '_________________'

    def normalize_price(self, raw_data):
        try:  # transforma 1.000, 00 em 1000.00
            raw_data = (raw_data[0]['content'].strip('R$ ') if len(raw_data) > 0 else '')
            raw_data = raw_data.replace('.', '').replace(',', '.')
            return float(raw_data)
        except ValueError:
            return 0.0

    def normalize_brand(self, raw_data):  # ["Samsung", "Asus", "Acer", "Dell", "Apple", "Positivo", "LG", "Lenovo"]

        if re.search('dell', raw_data, re.IGNORECASE) != None:
            return self.brands.get_dell()
        elif re.search('asus', raw_data, re.IGNORECASE) != None:
            return self.brands.get_asus()
        elif re.search('apple', raw_data, re.IGNORECASE) != None:
            return self.brands.get_apple()
        elif re.search('acer', raw_data, re.IGNORECASE) != None:
            return self.brands.get_acer()
        elif re.search('samsung', raw_data, re.IGNORECASE) != None:
            return self.brands.get_samsung()
        elif re.search('positivo', raw_data, re.IGNORECASE) != None:
            return self.brands.get_positivo()
        elif re.search('lenovo', raw_data, re.IGNORECASE) != None:
            return self.brands.get_lenovo()
        elif re.search('lg', raw_data, re.IGNORECASE) != None:
            return self.brands.get_lg()

    def normalize_processor(self, raw_data):
        raw_data = re.sub('\\\u\w\w\w\w', '', raw_data)

        if re.search('i3', raw_data, re.IGNORECASE) != None:
            return self.processors.get_i3()
        elif re.search('i5', raw_data, re.IGNORECASE) != None:

            return self.processors.get_i5()
        elif re.search('i7', raw_data, re.IGNORECASE) != None:

            return self.processors.get_i7()
        elif re.search('Pentium', raw_data, re.IGNORECASE) != None:

            return self.processors.get_pentium_quad()
        elif re.search('byt|baytrail', raw_data, re.IGNORECASE) != None:

            return self.processors.get_baytrail()
        elif re.search('amd.+dual core', raw_data, re.IGNORECASE) \
            != None:

            return self.processors.get_amd_dual()
        elif re.search('atom', raw_data, re.IGNORECASE) != None:

            return self.processors.get_atom()
        elif re.search('Intel.+Core.+M', raw_data, re.IGNORECASE) \
            != None:

            return self.processors.get_core_m()
        elif re.search('Celeron', raw_data, re.IGNORECASE) != None:

            return self.processors.get_celeron()
        elif re.search('arm', raw_data, re.IGNORECASE) != None:

            return self.processors.get_arm_a9()
        elif re.search('samsung', raw_data, re.IGNORECASE) != None:

            return self.processors.get_samsung()
