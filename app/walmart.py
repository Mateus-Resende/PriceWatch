from helpers.http_client import HttpClient
from helpers.processors import Processors
from helpers.mongo_client import MongoDB
from models.casas_bahia.data_extractor import DataExtractor
import json

class WalmartScraper(object):
    db = MongoDB()
    http = HttpClient()
    links_file = open("models/casas_bahia/list_links.json")
    invalid_links_file = open("models/walmart/invalid_links.json")

    def __init__():
        urls_string = links_file.read()
        links_file.close()
        products_urls = json.loads(urls_string)
        data = []

    for product_url in products_urls:
        response = http.get_request(product_url['link'])
        data_extractor = DataExtractor(response, product_url['link'])
        db.insert(data_extractor.parse())