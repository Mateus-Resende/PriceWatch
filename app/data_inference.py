from helpers.mongo_client import MongoDB
import collections
import pdb


"""Global variables"""
client = MongoDB()
db = client.get_db()


def run():
    create_parent_by_sku()
    create_parent_by_attributes()
    create_parent_by_inference()


def create_parent_by_sku():
    skus = filter(None, db.products.distinct('sku'))
    diversion_index = 0

    for sku in skus:
        if (db.products.count({"sku": sku}) > 1):
            products = db.products.find({"sku": sku, 'processed': False})
            parent = create_parent_product(list(products), diversion_index)
            if parent != None:
                db.parents.insert(parent)


def create_parent_by_attributes():
    brands = filter(None, db.products.distinct('brand'))

    for brand in brands:
        query = {'processed': False}
        query['brand'] = str(brand)
        processors = filter(None, db.products.distinct('processor', query))

        for processor in processors:
            query['processor'] = str(processor)
            ram_memories = filter(None, db.products.distinct('ram_memory', query))

            for ram_memory in ram_memories:
                query['ram_memory'] = str(ram_memory)
                storages = filter(None, db.products.distinct('storage', query))

                for storage in storages:
                    query['storage'] = str(storage)
                    display_sizes = filter(None, db.products.distinct('display_size', query))

                    for display_size in display_sizes:
                        query['display_size'] = str(display_size)
                        query['processed'] = False
                        products = db.products.find(query)
                        if products.count() >= 0:
                            parent = create_parent_product(list(products), 1)
                            if parent != None:
                                db.parents.insert(parent)


def create_parent_by_inference():
    attributes = ['brand', 'processor', 'ram_memory', 'storage', 'display_size']
    count = 4

    for i in range(len(attributes)):
        create_parent_from_four_attributes(attributes[:count] + attributes[count + 1:])
        count -= 1


def create_parent_from_four_attributes(attributes):
    query = {'processed': False}
    values0 = filter(None, db.products.distinct(attributes[0], query))

    for value0 in values0:
        query = {'processed': False}
        query[attributes[0]] = value0
        values1 = filter(None, db.products.distinct(attributes[1], query))

        for value1 in values1:
            query[attributes[1]] = value1
            values2 = filter(None, db.products.distinct(attributes[2], query))

            for value2 in values2:
                query[attributes[2]] = value2
                values3 = filter(None, db.products.distinct(attributes[3], query))

                for value3 in values3:
                    query[attributes[3]] = value3
                    products = db.products.find(query)
                    parent = create_parent_product(list(products), 2)
                    if parent != None:
                        db.parents.insert(parent)


def create_parent_product(products, diversion_index):
    if products == None or len(products) <= 0:
        return None
    else:
        parent_product = {}

        parent_product['storage'] = get_attribute(products, 'storage')
        parent_product['name'] = get_attribute(products, 'name')
        parent_product['processor'] = get_attribute(products, 'processor')
        parent_product['ram_memory'] = get_attribute(products, 'ram_memory')
        parent_product['display_size'] = get_attribute(products, 'display_size')
        parent_product['brand'] = get_attribute(products, 'brand')
        try:
            parent_product['model'] = get_attribute(products, 'model')
        except KeyError, e:
            pass
        parent_product['children'] = get_children_products(products)
        parent_product['stores'] = get_stores(products)
        parent_product['diversion_index'] = diversion_index

        return parent_product


def get_attribute(products, attr_name):
    if (len(products) > 0):
        for product in products:
            if product[attr_name.encode('ascii')] != None:
                return product[attr_name]
    else:
        return products[0][attr_name]


def get_children_products(products):
    children = []
    for product in products:
        children.append(product[u'_id'])
        db.products.update({'_id': product[u'_id']}, {"$set": {"processed": True}}, True, False)
    return children


def get_stores(products):
    stores = []

    for product in products:
        store = {}
        store['sku'] = product[u'sku']
        store['available'] = product[u'available']
        store['url'] = product[u'url']
        store['price'] = product[u'price']
        store['name'] = product[u'name']
        store['retailer'] = product[u'store']
        stores.append(store)

    return stores


run()
