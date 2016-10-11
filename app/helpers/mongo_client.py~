# coding: utf-8
from pymongo import MongoClient

# classe intermediária entre o banco de dados e os scripts
class MongoDB:

  # variável contendo o banco
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.price_watch
        #self.db.products.all_stores.create_index([("store", 1), ("sku", 1)], unique=True)


    # método de inserção simples, apenas um dado inserido por vez
    def insert(self, datum):
        return self.db.products.insert(datum)

    # método de inserção múltipla, vários dados inseridos por vez
    def bulk_insert(data):
        return self.db.products.insert_many(data)
	
	# método que compara se um produto com determinadas características já existe, se sim atualiza o seu vetor de lojas, se não simplesmente adiciona com
	# a primeira loja
    def insert_stores_in_products(self, data):
		
		dt = {}
		
		for key, value in data.items():
			dt[key] = value
		
		store = {}
		prod = {}
				
		store['price'] = dt['price']
		store['sku'] = dt['sku']
		store['store'] = dt['store']
		store['available'] = dt['available']
		store['url'] = dt['url']
		
		# principais para pesquisa
		prod['ram_memory'] = dt['ram_memory']
		prod['processor'] = dt['processor']
		prod['display_size'] = dt['display_size']
		prod['brand'] = dt['brand']
		# outros atributos coletados
		prod['name'] = dt['name']
		prod['storage'] = dt['storage']
		
		# cursor que irá listar todos os produtos com as quatro características
		# para fazer a inferência na atualização logo abaixo, o método find deve ter uma quantidade de itens razoável
		# pois não queremos que ele encontre mais de 1 item, pois para inferir metadados devemos comparar dois itens por vez...
		# o que foi encontrado no banco e o que está sendo inserido.
		cursor = self.db.products.find({'ram_memory':prod['ram_memory'], 'processor':prod['processor'], 'display_size':prod['display_size'], 'brand':prod['brand']})
		
		# se o produto já existe então adiciona a loja
		product = next(cursor, None)
		if product:
			print("Produto com estas características JÁ existe!")
			print("Adicionando LOJA in all_stores...")
			self.db.products.update(
				{ "_id": product["_id"] },
				{ "$addToSet": { "all_stores": store }
			})
		# se o produto não existe, então primeiro adiciona o produto e em seguida, adiciona a primeira loja
		else:
			print("Produto com estas características NÃO existe!")
			print("Adicionando produto in products...")
			_id = self.insert(prod)
			self.db.products.update(
				{ "_id" : _id },
				{ "$push": { "all_stores" : store}
			})
