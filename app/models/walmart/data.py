# -*- coding: utf-8 -*-
import re
from helpers.http_client import HttpClient
from helpers.data_list import DataList

class SpiderCasasBahia():

  def __init__(self, response, url):
    self.response = response
    self.url = url

  def parse(self):
    data = {}

    data['name'] = self.response.xpath('//*[@itemprop="name"]/text()')[0].strip()
    data['color'] = self.response.xpath('//*[@class="Cor"]/dd/text()')[0].strip()
    data['display_size'] = self.response.xpath('//*[@class="Tamanho-da-tela even"]/dd/text()')[0].strip()
    data['display_feature'] = self.response.xpath('//*[@class="Tipo-de-tela even"]/dd/text()')
    data['processor'] = self.response.xpath('//*[@class="Processador even"]/dd/text()')
    data['graphics_processor'] = self.response.xpath('//*[@class="Placa-de-video even"]/dd/text()')[0].strip()
    data['operating_system'] = self.response.xpath('//*[@class="Sistema-operacional"]/dd/text()')[0].strip()
    data['ram_memory'] = self.response.xpath('//*[@class="Memoria-RAM even"]/dd/text()')[0].strip()
    data['url'] = self.url
    data['image_url'] = self.response.xpath('//*[@itemprop="image"]//image/@src')
    storage = self.get_storage()
    if storage != None: data['storage'], data['storage_type'] = storage
    money_value = self.get_availability()
    data['available'], data['price'] = money_value
    data['brand'] = self.get_brand(data['name'])

    return data

  def get_storage(self):
    ssd = self.response.xpath('//*[@class="Memoria-Flash--SSD-"]/dd/text()')[0].strip()
    hd = self.response.xpath('//*[@class="Disco-rigido--HD-"]/dd/text()')[0].strip()

    # se não tiver ssd
    if (re.search('N.o se aplica', ssd) == None):
      return ['hd', hd]

    # se não tiver hd
    elif (re.search('N.o se aplica', hd) == None):
      return ['ssd', ssd]

    return None


  def get_availability(self):
    price = self.response.xpath('//*[@class="sale price"]/text()')[0].strip()
    price = re.sub('\,', '.', price)
    try:
      float(price)
      return [True, price]
    except ValueError:
      return [False, 0]

  def get_brand(self, product_name):
    data_list = DataList()
    brands_regex = data_list.get_brands_regex()
    return re.search(brands_regex, product_name)


