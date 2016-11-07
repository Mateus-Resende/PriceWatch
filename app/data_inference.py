from helpers.mongo_client import MongoDB
import collections
import pdb


"""Global variables"""
client = MongoDB()
db = client.get_db()


def run():
    create_parent_by_sku()
    create_parent_by_attributes()


def create_parent_by_sku():
    skus = filter(None, db.products.distinct('sku'))
    diversion_index = 0

    for sku in skus:
        if (db.products.count({"sku": sku}) > 1):
            products = db.products.find({"sku": sku})
            parent = create_parent_product(list(products), diversion_index)
            db.parent_prds.insert(parent)


def create_parent_by_attributes():
    brands = filter(None, db.products.distinct('brand'))

    for brand in brands:
        query = {}
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
                        products = db.products.find(query)
                        parent = create_parent_product(list(products), 1)
                        db.parent_prds.insert(parent)


def create_parent_product(products, diversion_index):
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
