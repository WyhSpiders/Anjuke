# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings

class CsanjukespiderPipeline(object):
    def __init__(self):
        self.host = settings['MONGO_HOST']
        self.port = settings['MONGO_PORT']
        self.db_name = settings['MONGO_DBNAME']

    def process_item(self, item, spider):
        client = pymongo.MongoClient(self.host, self.port)
        db = client[self.db_name]
        colection = db['anjuke']
        colection.insert(dict(item))
        return item
