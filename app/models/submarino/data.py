# -*- coding: utf-8 -*-
import re
from helpers.http_client import HttpClient
from helpers.data_list import DataList

class SpiderLojasAmericanas():

  def __init__(self, response, url):
    self.response = response
    self.url = url

  def parse(self):
    data = {}

    data['name'] = self.response.xpath('//*[@itemprop="name"]/text()')[0].strip()
    data['color'] = self.response.xpath('//*[@id="productdetails"]/div[3]/section/table/tr[3]/td/text()')[0].strip()
    data['display_size'] = self.response.xpath('//*[@id="productdetails"]/div[3]/section/table/tr[4]/td/text()')[0].strip()
    data['processor'] = self.response.xpath('//*[@id="productdetails"]/div[3]/section/table/tr[6]/td/text()')
    data['graphics_processor'] = self.response.xpath('//*[@id="productdetails"]/div[3]/section/table/tr[12]/td/text()')[0].strip()
    data['operating_system'] = self.response.xpath('//*[@id="productdetails"]/div[3]/section/table/tr[5]/td/text()')[0].strip()
    data['ram_memory'] = self.response.xpath('//*[@id="productdetails"]/div[3]/section/table/tbody/tr[9]/td/text()')[0].strip()
    data['url'] = self.url
    data['image_url'] = self.response.xpath('/html/body/div[6]/section/div/div[2]/div[1]/div[2]/figure/img')
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

