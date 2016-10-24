# coding: utf-8

from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.submarino.data_extractor import DataExtractor
from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from pymongo.errors import DuplicateKeyError

import json

db = MongoDB()
# http = HttpClient()
links_file = open("models/submarino/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)
#products_urls = ["http://www.submarino.com.br/produto/128878525/notebook-lenovo-ideapad-310-intel-core-i3-4gb-1tb-led-14-windows-10-prata#informacoes-tecnicas"]

# output = open("models/submarino/products.json", "wb")
data = []

for product_url in products_urls:
    try:
        bs_obj = BeautifulSoup(urlopen(product_url['link']).read(), "lxml")
        data_extractor = DataExtractor(bs_obj, product_url['link'])
        datum = data_extractor.parse()
        db.insert(datum)
    except HTTPError:
        continue
    except DuplicateKeyError:
        continue
