# coding: utf-8

from helpers.http_client import HttpClient
from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.casas_bahia.data_extractor import DataExtractor
import json

db = MongoDB()
http = HttpClient()
links_file = open("models/casas_bahia/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

# output = open("models/casas_bahia/products.json", "wb")
data = []

for product_url in products_urls:
    response = http.get_request(product_url['link'])
    data_extractor = DataExtractor(response, product_url['link'])
    datum = data_extractor.parse()
    # data.push(datum)
    db.insert(datum)


# output.write(json.dumps(data))
# output.close()

# print "Is datum valid? " + str(db.insert(datum))

