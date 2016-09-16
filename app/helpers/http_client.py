# -*- coding: utf-8 -*-

from lxml import html
import json
import requests

class HttpClient:

  def get_request(self, url):
    return html.fromstring(requests.get(url).content)

  def get_element_by_xpath(self, tree, xpath_string):
    return tree.xpath(xpath_string)[0].strip()
