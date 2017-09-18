# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class stockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stockName = scrapy.Field()
    stockCode = scrapy.Field()
    exchange = scrapy.Field()

class userItem(scrapy.Item):
	userName = scrapy.Field()
	userId = scrapy.Field()

class postItem(scrapy.Item):
	title = scrapy.Field()
	userId = scrapy.Field()
	stockId = scrapy.Field()
	postId = scrapy.Field()
	content = scrapy.Field()
	postTime = scrapy.Field()
	forwardCount = scrapy.Field()

class commentItem(scrapy.Item):
	userId = scrapy.Field()
	stockId = scrapy.Field()
	commentTime = scrapy.Field()
	content = scrapy.Field()
	commentId = scrapy.Field()
	postId = scrapy.Field()
	relatedTime = scrapy.Field()
