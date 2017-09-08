# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import pymongo

class StocksPipeline(object):
    def __init__(self):
        self.file=codecs.open("Stocks.json",mode="wb",encoding='utf-8')
        self.file.write('{"hah"'+':[')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))+","
        self.file.write(line.decode("unicode_escape"))

        return item

class MongoPipeline(object):
	"""docstring for MongoPipeline"""
	def __init__(self, mongo_url, mongo_port, mongo_db, mongo_collection):
		self.mongo_url = mongo_url
		self.mongo_port = mongo_port
		self.mongo_db = mongo_db
		self.mongo_collection = mongo_collection

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
				mongo_url = crawler.settings.get('MONGO_URL'),
				mongo_port = crawler.settings.get('MONGO_PORT'),
				mongo_db = crawler.settings.get('MONGO_DB'),
				mongo_collection = crawler.settings.get('MONGO_COLLECTION')
			)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(host = self.mongo_url, port = self.mongo_port)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		self.db[self.mongo_collection].insert_one(dict(item))
		return item
