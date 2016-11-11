# coding: utf-8

from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.submarino.data_extractor import DataExtractor
from urllib2 import urlopen
from bs4 import BeautifulSoup
from urllib2 import HTTPError
from pymongo.errors import DuplicateKeyError
from tqdm import tqdm

import json

db = MongoDB()
# http = HttpClient()
links_file = open("models/submarino/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)
# products_urls = ["http://www.submarino.com.br/produto/128878525/notebook-lenovo-ideapad-310-intel-core-i3-4gb-1tb-led-14-windows-10-prata#informacoes-tecnicas"]

# output = open("models/submarino/products.json", "wb")
data = []

for product_url in tqdm(products_urls):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8,pt;q=0.6',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Cookie': 'MobileOptOut=1; b2wDevice=eyJvcyI6IkxpbnV4Iiwib3NWZXJzaW9uIjoieDg2XzY0IiwidmVuZG9yIjoiQ2hyb21lIiwidHlwZSI6ImRlc2t0b3AiLCJta3ROYW1lIjoiQ2hyb21lIDUzIiwibW9kZWwiOiI1MyIsIm1vYmlsZU9wdE91dCI6ImZhbHNlIn0=; b2wDeviceType=desktop; catalogTestAB=out; catalog.source=zion; record=false; b2wChannel=INTERNET',
           'DNT': 1,
           'Host': 'www.submarino.com.br',
           'If-None-Match': 'W/\"7231b-P3i1qB58IwTsZdW2JhP6LQ',
           'Upgrade-Insecure-Requests': '0'
           }

    bs_obj = BeautifulSoup(urlopen(product_url['link']).read(), "lxml")
    data_extractor = DataExtractor(bs_obj, product_url['link'])
    datum = data_extractor.parse()
    db.insert(datum)
