# coding: utf-8

from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.havan.data_extractor import DataExtractor
from urllib2 import urlopen
from bs4 import BeautifulSoup

import json

db = MongoDB()
#http = HttpClient()
links_file = open("models/havan/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

output = open("models/havan/products.json", "wb")
data = []

for product_url in products_urls:
    bs_obj = BeautifulSoup(urlopen(product_url['link']).read(), "lxml")
    data_extractor = DataExtractor(bs_obj, product_url['link'])
    datum = data_extractor.parse()
    db.insert(datum)
