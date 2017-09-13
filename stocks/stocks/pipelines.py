# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pymongo

# import logging
# from scrapy.utils.log import configure_logging

# configure_logging(install_root_handler=False)
# logging.basicConfig(
#     filename='./log.log',
#     format='%(levelname)s: %(message)s',
#     level=logging.WARNING
# )

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
		self.collection = self.db[self.mongo_collection]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		item_dict = dict(item)
		old_one = self.collection.find_one({"stockCode": item_dict["stockCode"], "exchange": item_dict["exchange"]})
		if old_one is None:
			self.collection.insert_one(item_dict)
		return item
