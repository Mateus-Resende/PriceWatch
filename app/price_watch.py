# coding: utf-8
from helpers.mongo_client import MongoDB
from helpers.http_client import HttpClient
from helpers.data_list import DataList
from models.casas_bahia.data import SpiderCasasBahia

db = MongoDB()
http = HttpClient()
url = 'http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Positivo-Stilo-One-XC3550-com-Intel-Atom-Quad-Core-2GB-32GB-SSD-Leitor-de-Cartoes-HDMI-Bluetooth-Webcam-LED-14-e-Windows-10-9233539.html'

response = http.get_request(url)
spider = SpiderCasasBahia(response, url)

datum = spider.parse()

print "Is datum valid? " + str(db.insert(datum))

