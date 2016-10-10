# coding: utf-8

from bs4 import BeautifulSoup
from helpers.mongo_client import MongoDB
from pymongo.errors import DuplicateKeyError
from models.walmart.data import DataExtractor
import urllib2
import json


db = MongoDB()

base_url = "https://www.walmart.com.br"
url = "https://www.walmart.com.br/categoria/informatica/notebooks-e-ultrabooks/?fq=C:4699/4701/&mm=100&originPath=informatica/notebooks-e-ultrabooks&PageNumber="
count = 1

req = urllib2.Request(url + str(count), headers={'User-Agent': "Magic Browser"})
bs_obj = BeautifulSoup(urllib2.urlopen(req), "lxml")
products = bs_obj.findAll("li", {"class": "shelf-product-item"})

print "found: ", len(products)

for product in products:

    product_url = base_url + product.a['href']
    print product_url
    product_req = urllib2.Request(product_url, headers={'User-Agent': "Magic Browser"})
    product_bs = BeautifulSoup(urllib2.urlopen(product_req), "lxml")
    data_extractor = DataExtractor(product_bs, product_url)
    try:
        data = data_extractor.parse()
        print data['model']
    except IndexError:
        print '-------- error!'
        continue

    print '##########\n'
