# coding: utf-8

from helpers.http_client import HttpClient
from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.eletrosom.data_extractor import DataExtractor
import json

db = MongoDB()
http = HttpClient()
links_file = open("models/eletrosom/list_links.json")

urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

for product_url in products_urls:
	response = http.get_request(product_url["link"])
	data_extractor = DataExtractor(response, product_url["link"])
	data = data_extractor.parse()
	db.insert(data)