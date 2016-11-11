# coding: utf-8

import urllib2
from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.shoptime.data_extractor import DataExtractor
from urllib2 import urlopen
from urllib2 import HTTPError
from pymongo.errors import DuplicateKeyError
from bs4 import BeautifulSoup
from tqdm import tqdm


import json

db = MongoDB()
# http = HttpClient()
links_file = open("models/shoptime/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

# output = open("models/casas_bahia/products.json", "wb")
data = []

for product_url in tqdm(products_urls):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(product_url['link'], headers=hdr)
        page = urllib2.urlopen(req)
        bs_obj = BeautifulSoup(page.read(), "lxml")
        data_extractor = DataExtractor(bs_obj, product_url['link'])
        datum = data_extractor.parse()
        db.insert(datum)
    except HTTPError:
        print "Http error"
        continue
    except DuplicateKeyError:
        print "Duplicate key error"
        continue
