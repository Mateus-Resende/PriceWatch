#!/bin/bash
scrapy runspider links.py -t json -o - > links_list.json

