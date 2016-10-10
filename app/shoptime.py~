# coding: utf-8

import urllib2
from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.shoptime.data_extractor import DataExtractor
from bs4 import BeautifulSoup

import json

db = MongoDB()
# http = HttpClient()
links_file = open("models/shoptime/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

# output = open("models/casas_bahia/products.json", "wb")
data = []

for product_url in products_urls:
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(product_url['link'],headers=hdr)
	page = urllib2.urlopen(req)
	bs_obj = BeautifulSoup(page.read(),"lxml")
	data_extractor = DataExtractor(bs_obj,product_url['link'])
	datum = data_extractor.parse()
	db.insert(datum)
