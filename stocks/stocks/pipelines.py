# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pymongo
from items import stockItem, userItem, postItem, commentItem

import logging
logger = logging.getLogger('pipelineslog')
# from scrapy.utils.log import configure_logging

# configure_logging(install_root_handler=False)
# logging.basicConfig(
#     filename='./log.log',
#     format='%(levelname)s: %(message)s',
#     level=logging.WARNING
# )
STOCK_LIST = 'stocks'
USER_LIST = 'users'
POST_LIST = 'posts'
COMMENT_LIST = 'comments'

class MongoPipeline(object):
	"""docstring for MongoPipeline"""
	def __init__(self, mongo_url, mongo_port, mongo_db):
		self.mongo_url = mongo_url
		self.mongo_port = mongo_port
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
				mongo_url = crawler.settings.get('MONGO_URL'),
				mongo_port = crawler.settings.get('MONGO_PORT'),
				mongo_db = crawler.settings.get('MONGO_DB')
			)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(host = self.mongo_url, port = self.mongo_port)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		if isinstance(item, stockItem):
			stock_dict = dict(item)
			collection = self.db[STOCK_LIST]
			if collection.find_one({"stockCode":stock_dict["stockCode"],"exchange":stock_dict["exchange"]}) is None:
				collection.insert_one(stock_dict)
		elif isinstance(item, userItem):
			user_dict = dict(item)
			collection = self.db[USER_LIST]
			if collection.find_one({"userId":user_dict["userId"]}) is None:
				collection.insert_one(user_dict)
		elif isinstance(item, postItem):
			post_dict = dict(item)
			collection = self.db[POST_LIST]
			if collection.find_one({"postId":post_dict["postId"]}) is None:
				collection.insert_one(post_dict)
		elif isinstance(item, commentItem):
			comment_dict = dict(item)
			collection = self.db[COMMENT_LIST]
			if collection.find_one({"commentId":comment_dict["commentId"], "postId":comment_dict["postId"]}) is None:
				related_time = comment_dict.pop("relatedTime", None)
				if related_time is not None:
					relatedComment = collection.find_one({"commentTime": related_time, "postId":comment_dict["postId"]})
					if relatedComment is not None:
						comment_dict["relatedId"] = relatedComment["commentId"]
						if "reply" in relatedComment:
							relatedComment["reply"].append(comment_dict["commentId"])
						else:
							relatedComment["reply"] = [comment_dict["commentId"]]
						collection.update_one({'_id':relatedComment["_id"]}, {"$set":{'reply':relatedComment["reply"]}});
				collection.insert_one(comment_dict)
			else:
				logger.warning('%s is already exist' % comment_dict["commentId"])
		else:
			pass
		return item
