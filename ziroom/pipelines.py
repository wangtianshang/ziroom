# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ZiroomPipeline(object):
    def __init__(self):
        self.c = pymongo.MongoClient()
        self.db = self.c['ziru']
    def process_item(self, item, spider):
        self.db['room'].insert(dict(item))
        return item
