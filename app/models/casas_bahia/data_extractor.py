# -*- coding: utf-8 -*-
import re
from helpers.http_client import HttpClient
from helpers.processors import Processors

class DataExtractor():

  def __init__(self, response, url):
    self.response = response
    self.url = url
    self.processors = Processors()


  def parse(self):
    data = {}

    data['processor'] = self.response.xpath('//*[@class="Processador"]/dd/text()')
    if (len(data['processor']) > 0): data['processor'] = self.normalize_processor(data['processor'][0].strip())

    return data


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
      
    return ""


