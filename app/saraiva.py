from tqdm import tqdm
# coding: utf-8

from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.saraiva.data_extractor import DataExtractor
from urllib2 import urlopen
from bs4 import BeautifulSoup

import json

print "Iniciando..."

db = MongoDB()
# http = HttpClient()
links_file = open("models/saraiva/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

data = []

print "\nColetando os dados... ^^"

for product_url in tqdm(products_urls):
    try:
        bs_obj = BeautifulSoup(urlopen(product_url['link']).read(), "lxml")
        data_extractor = DataExtractor(bs_obj, product_url['link'])
        datum = data_extractor.parse()
        db.insert(datum)
    except Exception, e:
        print e
        continue

print "\nFinalizado! :D"
