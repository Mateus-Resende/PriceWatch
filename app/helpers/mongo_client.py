# coding: utf-8
from pymongo import MongoClient

# classe intermediária entre o banco de dados e os scripts


class MongoDB:

  # variável contendo o banco
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.price_watch
        self.db.products.create_index([("store", 1), ("sku", 1)], unique=True)

    # método de inserção simples, apenas um dado inserido por vez
    def insert(self, datum):
        if datum["sku"] != None and datum["sku"] != "" and datum["store"] != None:
            datum['processed'] = False
            return self.db.products.insert_one(datum)

    def find_one(self, store, id):
        return self.db.products.find_one({store: store, sku: id})

    def find_query(self, query_string):
        return self.db.products.find({query_string})

    # método de inserção múltipla, vários dados inseridos por vez
    def bulk_insert(data):
        return self.db.products.insert_many(data)

    def get_db(self):
        return self.db
