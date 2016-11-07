# coding: utf-8

from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.casas_bahia.data_extractor import DataExtractor
from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from pymongo.errors import DuplicateKeyError
from tqdm import tqdm

import json

db = MongoDB()
# http = HttpClient()
links_file = open("models/casas_bahia/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

# output = open("models/casas_bahia/products.json", "wb")
data = []

for product_url in tqdm(products_urls):
    try:
        bs_obj = BeautifulSoup(urlopen(product_url['link']).read(), "lxml")
        data_extractor = DataExtractor(bs_obj, product_url['link'])
        datum = data_extractor.parse()
        db.insert(datum)
    except HTTPError:
        print '## HTTP Error!'
        continue
    except DuplicateKeyError:
        print '## Duplicate Key Error'
        continue
