# coding: utf-8
from pymongo import MongoClient

# classe intermediária entre o banco de dados e os scripts
class MongoDB:

  # variável contendo o banco
  def __init__(self):
    self.client = MongoClient()
    self.db = self.client.PriceWatch

  # método de inserção simples, apenas um dado inserido por vez
  def insert(self, datum):
    inserted = False
    
    if self.is_valid(datum):
      self.db.products.insert_one(datum)
      inserted = True  

    return inserted

  # método de inserção múltipla, vários dados inseridos por vez
  def bulk_insert(data):
    return self.db.products.inser_many(data)

  def is_valid(self, datum):
    return (True if (datum['name'] and datum['url'] and 
                      datum['brand'] and datum['storage'] and 
                      datum['ram_memory'] and datum['display_size'] 
                      and datum['sku']) else False)

