# coding: utf-8
from helpers.mongo_client import MongoDB
from helpers.http_client import HttpClient
from helpers.processors import Processors
from models.casas_bahia.data_extractor import DataExtractor
import json

db = MongoDB()
http = HttpClient()
links_file = open("models/casas_bahia/list_links.json")

urls_string = '[{"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Acer-Aspire-E5-574-307M-com-Intel-Core-i3-6100U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-Bluetooth-LED-15-6-e-Windows-10-7487001.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Acer Aspire E5-574-307M com Intel\u00ae Core\u2122 i3-6100U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, Bluetooth, LED 15.6&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Positivo-Stilo-One-XC3550-com-Intel-Atom-Quad-Core-2GB-32GB-SSD-Leitor-de-Cartoes-HDMI-Bluetooth-Webcam-LED-14-e-Windows-10-9233539.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Positivo Stilo One XC3550 com Intel\u00ae Atom\u00ae Quad Core, 2GB, 32GB SSD, Leitor de Cart\u00f5es, HDMI, Bluetooth, Webcam, LED 14&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Samsung-Essentials-E32-370E4K-KW3-com-Intel-Core-i3-5005U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-Webcam-LED-14-e-Windows-10-5701251.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Samsung Essentials E32 370E4K-KW3 com Intel\u00ae Core\u2122 i3-5005U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, Webcam, LED 14&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Lenovo-G40-80-com-Intel-Core-i3-5005U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-Wireless-Bluetooth-LED-14-e-Windows-10-6487594.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Lenovo G40-80 com Intel\u00ae Core\u2122 i3-5005U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, Wireless, Bluetooth, LED 14&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Dell-Inspiron-I14-5458-D08P-com-Intel-Core-i3-5005U-4GB-1TB-Leitor-de-Cartoes-HDMI-Wireless-Bluetooth-Webcam-LED-14-e-Linux-8307376.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Dell Inspiron I14-5458-D08P com Intel\u00ae Core\u2122 i3-5005U, 4GB, 1TB, Leitor de Cart\u00f5es, HDMI, Wireless, Bluetooth, Webcam, LED 14&quot; e Linux"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Dell-Inspiron-I15-5558-B10B-com-Intel-Core-i3-4005U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-Bluetooth-LED-15-6-e-Windows-10-7305578.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Dell Inspiron I15-5558-B10B com Intel\u00ae Core\u2122 i3-4005U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, Bluetooth, LED 15.6&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Samsung-Essentials-E33-270E5K-KW1-com-Intel-Core-i3-5005U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-LED-15-6-e-Windows-10-5701256.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Samsung Essentials E33 270E5K-KW1 com Intel\u00ae Core\u2122 i3-5005U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, LED 15.6&quot; e Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Lenovo-G40-80-com-Intel-Core-i5-5200U-4GB-1TB-Gravador-de-DVD-Leitor-de-Cartoes-HDMI-Wireless-Bluetooth-Webcam-LED-14-Windows-10-5875999.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Lenovo G40-80 com Intel\u00ae Core\u2122 i5-5200U, 4GB, 1TB, Gravador de DVD, Leitor de Cart\u00f5es, HDMI, Wireless, Bluetooth, Webcam, LED 14&quot;, Windows 10"}, {"link": "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Positivo-Stilo-XR5550-com-Intel-Pentium-N3540-Quad-Core-4GB-500GB-Leitor-de-Cartoes-HDMI-Wireless-Webcam-LED-14-e-Windows-10-5387530.html?recsource=busca-int&rectype=busca-57", "name": "Notebook Positivo Stilo XR5550 com Intel\u00ae Pentium\u00ae N3540 Quad Core, 4GB, 500GB, Leitor de Cart\u00f5es, HDMI, Wireless, Webcam, LED 14&quot; e Windows 10"}]'

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

