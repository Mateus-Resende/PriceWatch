# coding: utf-8
from helpers.processors import Processors
from helpers.comparator import Comparator
from helpers.mongo_client import MongoDB
import json

db_original = MongoDB()
db_comparator = Comparator()

cursor = db_original.find()

for product in cursor:
    db_comparator.compare_it(product)
