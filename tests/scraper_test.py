# -*- coding: utf-8 -*-

from lxml import html
import json
import requests

# inicialização do JSON que receberá os dados coletados
# JSON é um tipo de variável que possui uma chave e um valor determinado à ela
# Essa chave é SEMPRE ÚNICA
# O valor pode repetir
data = {}

# utilização de url de produto das casas bahia como exemplo
sample_url = "http://www.casasbahia.com.br/Informatica/Notebook/Notebook-Positivo-Stilo-One-XC3550-com-Intel-Atom-Quad-Core-2GB-32GB-SSD-Leitor-de-Cartoes-HDMI-Bluetooth-Webcam-LED-14-e-Windows-10-9233539.html"

# fazendo requisição HTTP com verbo GET para a url dada
product_page = requests.get(sample_url)

# leitura do conteúdo da página
tree = html.fromstring(product_page.content)

# Leitura dos dados da página de acordo com o xpath dado
# Reparem que uso o html+css da página para reconhecer um elemento desejado
data['name'] = tree.xpath("//b[@itemprop='name']/text()")[0].strip()
data['price'] = tree.xpath("//i[@class='sale price']/text()")[0].strip()
data['processor'] = tree.xpath('//*[@class="Processador"]/dd/text()')[0].strip()
data['screen_size'] = tree.xpath('//dl[@class="Tamanho-da-tela even"]/dd/text()')[0].strip()
data['operational_system'] = tree.xpath('//*[@class="Sistema-operacional"]/dd/text()')[0].strip()
data['color'] = tree.xpath('//*[@class="Cor"]/dd/text()')[0].strip()
data['ram_memory'] = tree.xpath('//*[@class="Memoria-RAM even"]/dd/text()')[0].strip()
data['battery'] = tree.xpath('//*[@class="Bateria even"]/dd/text()')[0].strip()

# Impressão dos dados na tela com identação de quatro espaços e ordenação
# das chaves do json
print json.dumps(data, indent=4, sort_keys=True)



