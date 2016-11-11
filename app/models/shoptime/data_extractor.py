#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from lxml import etree
from helpers.processors import Processors
from helpers.brands import Brands
from helpers.memory import Memory
from helpers.storages import Storages
from bs4 import BeautifulSoup


class DataExtractor:

    def __init__(self, response, url):
        self.response = response
        self.url = url
        self.processors = Processors()
        self.brands = Brands()
        self.memory = Memory()
        self.storages = Storages()

    def parse(self):

        data = {}

        r = self.response

        # produtos da shoptime
        data['store'] = 'shoptime'

        # nome do produto
        try:
            data['name'] = r.find('h1', {'id': 'main-product-name'})
            data['name'] = self.validate_field(data, 'name')
            data['name'] = re.sub(re.compile(u' \(Cód\. ([0-9])+\)'), '', data['name'])
        except (ValueError, TypeError, AttributeError):
            data['name'] = ''

            # url como variavel global da classe
        data['url'] = self.url

        # preço do produto
        try:
            data['price'] = r.find('span', {'data-partner-value': True})['data-partner-value']
            data['price'] = self.normalize_price(data['price'])
        except (ValueError, TypeError, AttributeError):
            data['price'] = 0.0

        # disponibilidade
        try:
            data['available'] = self.set_available(r, data['price'])
        except (ValueError, TypeError, AttributeError):
            data['available'] = False

        try:
            # processador
            data['processor'] = r.find('th', text=re.compile(r'Processador')).parent.find('td').text
            data['processor'] = self.normalize_processor(data['processor'])
        except (ValueError, TypeError, AttributeError):
            data['processor'] = ''

        # marca
        try:
            data['brand'] = r.find('th', text=re.compile(r'Marca')).parent.find('td').text
            data['brand'] = (self.normalize_brand(data['name'])).strip()
        except (ValueError, TypeError, AttributeError):
            data['brand'] = ''

            # memória ram
        try:
            data['ram_memory'] = r.find('th', text=re.compile(u'Memória RAM')).parent.find('td').text
        except (ValueError, TypeError, AttributeError):
            data['ram_memory'] = ''

            # sku para identificação
        try:
            data['sku'] = r.find('div', {'data-sku': True})['data-sku']
        except (ValueError, TypeError, AttributeError):
            data['sku'] = ''

        # armazenamento (SSD/HD)
        try:

            try:
                hd = r.find('th', text=re.compile(r'HD')).parent.find('td').text
            except (ValueError, TypeError, AttributeError):
                hd = ''

            try:
                ssd = r.find('th', text=re.compile(r'SSD')).parent.find('td').text
            except (ValueError, TypeError, AttributeError):
                ssd = ''

            data['storage'] = self.normalize_storage(hd, ssd)
        except (ValueError, TypeError, AttributeError):
            data['storage'] = self.normalize_storage('', '')

        # tamanho da tela
        try:
            data['display_size'] = self.normalize_display_size(r.find('th', text=re.compile(r'Polegadas da Tela')).parent.find('td').text)
        except (ValueError, TypeError, AttributeError):
            data['display_size'] = ''

        try:
            data['img_url'] = (r.findAll('img', {'class': 'p-image'})[0]['src']).strip()
        except (ValueError, TypeError, AttributeError, IndexError):
            data['img_url'] = ''

        return data

    def set_available(self, response, price):
        meta = response.find('div', {'class': 'product-unavailable'})
        if (meta == None) and (price != 0.0):
            return True
        else:
            return False

    def validate_field(self, data, field):
        if data[field] != None:
            return (data[field].get_text().strip() if (len(data[field]) > 0) else '')

    def normalize_display_size(self, text):
        if text != None and len(text) > 0:
            return (text.strip(" \"").replace(",", ".") + "\"").strip()
        else:
            return ''

    def normalize_storage(self, hd, ssd):
        result = ''
        if hd != None and len(hd) > 0:
            result = re.search('\d+.+[TG]B', hd)
            if result != None:
                return self.get_storage_capacity(result.group())

        if ssd != None and len(ssd) > 0:
            result = re.search('\d+.+[TG]B', ssd)
            if result != None:
                return self.get_storage_capacity(result.group())

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

    def normalize_price(self, raw_data):
        try:  # transforma 1.000, 00 em 1000.00
            raw_data = (raw_data if len(raw_data) > 0 else '')
            price = float(raw_data)
            price = round(price, 2)
            return price
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
        elif re.search('compaq', raw_data, re.IGNORECASE) != None:
            return self.brands.get_compaq()
        elif re.search('seagate', raw_data, re.IGNORECASE) != None:
            return self.brands.get_seagate()
        elif re.search('gigabyte', raw_data, re.IGNORECASE) != None:
            return self.brands.get_gigabyte()
        elif (re.search('hp', raw_data, re.IGNORECASE) != None):
            return self.brands.get_hp()
        elif (re.search('sony', raw_data, re.IGNORECASE) != None):
            return self.brands.get_sony()

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

    # normalização de capacidade
    def get_storage_capacity(self, raw_data):
        if (re.search('2TB|2 TB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_2tb()

        elif (re.search('1TB|1 TB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_1tb()

        elif (re.search('750 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_750()

        elif (re.search('640 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_640()

        elif (re.search('500 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_500()

        elif (re.search('320GB|320 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_320()

        elif (re.search('256GB|256 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_256()

        elif (re.search('160GB|160 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_160()

        elif (re.search('128GB|128 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_128()

        elif (re.search('80GB|80 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_80()

        elif (re.search('64GB|64 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_64()

        elif (re.search('32GB|32 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_32()

        elif (re.search('16GB|16 GB', raw_data, re.IGNORECASE) != None):
            return self.storages.get_16()
