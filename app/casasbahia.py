# coding: utf-8
# from helpers.mongo_client import MongoDB
from helpers.http_client import HttpClient
from helpers.processors import Processors
from models.casas_bahia.data_extractor import DataExtractor
import json

# db = MongoDB()
http = HttpClient()
links_file = open("models/casas_bahia/list_links.json")

urls_string = '[{"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Acer-Aspire-E5-574-307M-com-Intel-Core-i3-6100U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-Bluetooth-LED-15-6-e-Windows-10-7487001.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Acer Aspire E5-574-307M com Intel\u00ae Core\u2122 i3-6100U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, Bluetooth, LED 15.6&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Positivo-Stilo-One-XC3550-com-Intel-Atom-Quad-Core-2GB-32GB-SSD-Leitor-de-Cartoes-HDMI-Bluetooth-Webcam-LED-14-e-Windows-10-9233539.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Positivo Stilo One XC3550 com Intel\u00ae Atom\u00ae Quad Core, 2GB, 32GB SSD, Leitor de Cart\u00f5es, HDMI, Bluetooth, Webcam, LED 14&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Samsung-Essentials-E32-370E4K-KW3-com-Intel-Core-i3-5005U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-Webcam-LED-14-e-Windows-10-5701251.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Samsung Essentials E32 370E4K-KW3 com Intel\u00ae Core\u2122 i3-5005U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, Webcam, LED 14&quot; e Windows 10"}]'

# urls_string = links_file.read()
links_file.close()

products_urls = json.loads(urls_string)

output = open("models/casas_bahia/processor_list.json", "wb")
data = []

for product_url in products_urls:
    response = http.get_request(product_url['link'])
    data_extractor = DataExtractor(response, product_url['link'])
    datum = data_extractor.parse()
    data.append(datum)


output.write(json.dumps(data))
output.close()

# print "Is datum valid? " + str(db.insert(datum))

