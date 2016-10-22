# -*- coding: utf-8 -*-
import re
from helpers.processors import Processors
from helpers.brands import Brands
from helpers.memory import Memory
from bs4 import BeautifulSoup


class DataExtractor():

    def __init__(self, response, url):
        self.response = response
        self.url = url
        self.processors = Processors()
        self.brands = Brands()
        self.memory = Memory()

    #{ _id, available, brand, color, display_feature, display_size, graphics_processor_name, graphics_processor, name, operating_system, price, processor, ram_memory, sku, screen_resolution, storage, storage_type, url, img_url}

    # TODO: display_feature, display_size, graphics_processor_name, graphics_processor, operating_system, screen_resolution, storage_type, img_url

    def parse(self):
        data = {}

        # produtos da havan
        data['store'] = "havan"

        # nome do produto
        data['name'] = self.response.findAll("", {"class": "product-qd-v1-name"})
        data['name'] = self.validate_field(data, 'name')

        # url como variavel global da classe
        data['url'] = self.url

        # preco do produto
        data['price'] = self.response.findAll("", {"class": "skuBestPrice"})
        data['price'] = self.normalize_price(data['price'])

        # disponibilidade: nas casas bahia, se o produto possuir preco, o produto esta disponivel
        data['available'] = data['price'] != None and data['price'] != 0.0

        # processador
        data['processor'] = self.response.findAll("", {"class": "value-field Modelo-do-Processador"})
        data['processor'] = self.normalize_processor(self.validate_field(data, 'processor'))

        # marca
        data['brand'] = self.normalize_brand(data['name'])

        # memoria ram
        data['ram_memory'] = self.response.findAll("td", {"class": "value-field Memoria-Fisica-Disponivel"})
        data['ram_memory'] = self.normalize_memory(self.validate_field(data, 'ram_memory'))

        # sku para identificacao
        data['sku'] = self.response.findAll("", {"class": "skuReference"})
        data['sku'] = self.validate_field(data, 'sku')

        # armazenamento (SSD/HD)
        data['storage'] = self.response.findAll("", {"class": "value-field Capacidade-do-Disco-Rigido-HD-"})
        data['storage'] = self.validate_field(data, 'storage')
        #ssd = self.response.findAll("", {"class": "value-field Unidade-de-Estado-Solida-SSD-"})

        # tamanho de tela
        display = self.response.findAll("td", {"class": "value-field Tamanho-da-Tela"})
        data['display_size'] = self.normalize_display(display) if (len(display) > 0) else ""

        return data

    def validate_field(self, data, field):
        return (data[field][0].get_text().strip() if (len(data[field]) > 0) else "")

    def normalize_memory(self, raw_data):
        if (re.search('16', raw_data, re.IGNORECASE) != None):
            return self.memory.get_16GB()
        elif (re.search('12', raw_data, re.IGNORECASE) != None):
            return self.memory.get_12GB()
        elif (re.search('14', raw_data, re.IGNORECASE) != None):
            return self.memory.get_14GB()
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
            # transforma 1.000,00 em 1000.00
            raw_data = raw_data[0].get_text() if (len(raw_data) > 0) else ""
            raw_data = raw_data.replace('.', '').replace(',', '.').replace('R$', '')
            return float(raw_data)
        except ValueError:
            return 0.0

    def normalize_display(self, raw_data):
        try:
            raw_data = raw_data[0].get_text() if (len(raw_data) > 0) else ""
            raw_data = raw_data.replace('"', '')
            return raw_data
        except ValueError:
            return ""

    def normalize_brand(self, raw_data):
        # ["Samsung", "Asus", "Acer", "Dell", "Apple", "Positivo", "LG", "Lenovo"]

        if (re.search('dell', raw_data, re.IGNORECASE) != None):
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
        # ['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intem Pentium Quad Core', 'Intel Baytrail', 'AMD Dual Core', 'Item Atom', 'Intel Core M', 'Intel Celeron']

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
