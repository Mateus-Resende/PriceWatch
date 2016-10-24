# coding: utf-8
from pymongo import MongoClient

# classe intermediária entre o banco de dados e os scripts
class Comparator:

  # variável contendo o banco
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.price_watch_comparator

    # método de inserção simples, apenas um dado inserido por vez
    def insert(self, datum):
        return self.db.products.insert(datum)

    def compare_it(self, data):
        dt, store, prod = {}, {}, {}

        for key, value in data.items():
            dt[key] = value

        store_features = ['price', 'sku', 'store', 'available', 'url']
        prod_features = ['ram_memory', 'processor', 'display_size', 'brand', 'name', 'storage']

        for key in store_features:
            store[key] = dt[key]
            
        for key in prod_features:
            prod[key] = dt[key]

        cursor = self.db.products.find({'ram_memory':prod['ram_memory'], 'processor':prod['processor'], 'display_size':prod['display_size'], 'brand':prod['brand']})
        
        product = next(cursor, None)

        parent_product = product
        parent_change = False
        
        for key in prod_features:
            if product:
                # produto que está no banco
                product_feature_invalid = (product[key] == None) or (product[key] == 0) or (product[key] == "") or (product[key] == 0.0)
                # produto que está para ser inserido
                prod_feature_invalid = (prod[key] == None) or (prod[key] == 0) or (prod[key] == "") or (prod[key] == 0.0)

                # se o produto que está no banco tem certa característica inválida...
                if product_feature_invalid:
                    # porém o produto que está para ser inserido possui está característica...
                    if (not prod_feature_invalid):
                        # então atualiza no produto pai
                        parent_product[key] = prod[key]
                        parent_change = True
                        print("Parent PRODUCT will change!")
        
        if parent_change:
            self.db.products.update(
                {"_id": parent_product["_id"]},
                {"$set":
                    {
                        'ram_memory': parent_product['ram_memory'],
                        'processor': parent_product['processor'],
                        'display_size': parent_product['display_size'],
                        'brand': parent_product['brand'],
                        'storage': parent_product['storage'],
                        'name': parent_product['name']
                    }
                }
            )

        try:
            if product:
                print("PRODUCT exists. Adding the STORE...")
                self.db.products.update(
                    { "_id": product["_id"] },
                    { "$addToSet": { "stores": store, "sub_products": prod }
                })
            else:
                print("PRODUCT not exists. Adding it...")
                _id = self.insert(prod)
                self.db.products.update(
                    { "_id" : _id },
                    { "$push": { "stores" : store, "sub_products": prod }
                })
        except:
            print("Update error!")
