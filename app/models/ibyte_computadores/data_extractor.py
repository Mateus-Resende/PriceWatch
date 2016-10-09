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

        # produtos das casas bahia
        data['store'] = "ibyte_computadores"

        # nome do produto
        data['name'] = self.response.findAll("li", {"class": "product"})
        data['name'] = self.validate_field(data, 'name')

        # url como variavel global da classe
        data['url'] = self.url

        # preco do produto
        data['price'] = self.response.findAll("span", {"id": "product-price-37429"})
        data['price'] = self.normalize_price(data['price'])

        # disponibilidade: nas casas bahia, se o produto possuir preco, o produto esta disponivel
        data['available'] = data['price'] != None and data['price'] != 0.0

        # processador incompleto
        data['processor'] = self.response.find("div", {"class": "std"})
        data['processor'] = self.normalize_processor(self.validate_field(data, 'processor'))

        # marca
        data['brand'] = self.normalize_brand(data['name'])

        # memoria ram
        data['ram_memory'] = self.response.findAll("dl", {"class": "Memoria-RAM"})
        data['ram_memory'] = self.normalize_memory(self.validate_field(data, 'ram_memory'))

        # sku para identificacao
        data['sku'] = self.url.split('?')[0].split('-')[-1].split('.')[0]

        # armazenamento (SSD/HD)
        hd = self.response.findAll("dl", {"class": "Disco-rigido--HD-"})
        ssd = self.response.findAll("dl", {"class": "Memoria-Flash--SSD-"})
        data['storage'] = self.normalize_storage(hd, ssd)

        # tamanho de tela
        data['display_size'] = self.response.findAll("dl", {"class": "Tamanho-da-tela"})
        data['display_size'] = data['display_size'][0].find('dd').get_text().strip() if (len(data["display_size"]) > 0) else ""

        return data

    def validate_field(self, data, field):
        return (data[field][0].get_text().strip() if (len(data[field]) > 0) else "")

    def normalize_storage(self, hd, ssd):
        if (len(hd) > 0):
            hd = hd[0].find('dd').get_text()
        if (len(ssd) > 0):
            ssd = ssd[0].find('dd').get_text()

        result = {}
        if hd != None and len(hd) > 0:
            result["HD"] = re.search('\d+.+[TG]B', hd)
            if result["HD"] != None:
                result["HD"] = result["HD"].group()

        if ssd != None and (len(ssd) > 0) and result == None:
            result["SSD"] = re.search('\d+.+[TG]B', ssd)
            if result["SSD"] != None:
                result["SSD"] = result["SSD"].group()

        return result

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
            raw_data = raw_data.replace('.', '').replace(',', '.')
            raw_data = raw_data.replace('R$', '').replace(',', '.')
            return float(raw_data)
        except ValueError:
            return 0.0

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