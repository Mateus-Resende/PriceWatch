# -*- coding: utf-8 -*-
class DataList:

  def is_valid_brand(self, string=""):
    return (string.lower() in self.get_brands_list())

  def get_brands_regex(self):
    return '/' + '|'.join(map(str, self.get_brands_list())) + '/'

  def get_brands_list(self):
    return ['acer', 'asus', 'apple', 'dell', 'hp', 'samsung']
