# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class DataExtractor():

    def __init__(self, response, url):
        self.response = response
        self.url = url

    def parse(self):
        data = {}

        data['store'] = 'walmart'

        data['name'] = self.response.findAll('h1', {'itemprop': 'name'})[0].contents[0]
        data['sku'] = self.response.findAll("button", {"class": "wishlist-button toolbar-button"})[0]['data-product']

        data['price'] = self.response.findAll("button", {"class": "wishlist-button toolbar-button"})[0]['data-price']

        data['available'] = data['price'] != None

        data['model'] = self.response.findAll("td", {"class": "Referencia-do-Modelo"})[0].contents[0]

        data['screen_size'] = self.response.findAll("td", {"class": "Tela"})[0].contents[0]

        return data
