from scrapy import Spider
from scrapy import Selector
from scrapy import Request
from stocks.items import stockItem, userItem, postItem, commentItem
import logging
import re

logger = logging.getLogger('mycustomlogger')

class gubaSpider(Spider):
    name = 'guba'
    site_domain = 'http://guba.eastmoney.com'
    allowed_domain = ['eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html#sh/']

    def parse(self, response):
        sel = Selector(response)
        url = 'http://guba.eastmoney.com/list,000858,99_1.html'
        logger.warning(url)

        yield Request(url, callback=self.parsecontent)


        # contsh=sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')[0].extract()
        # for stockSH in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>',contsh):
        #     if (stockSH.split("(")[1][:-1]).encode('utf-8').startswith('20'):
        #         continue
        #     item["stockName"] = stockSH.split("(")[0].encode('utf-8')
        #     item["stockCode"]=(stockSH.split("(")[1][:-1]).encode('utf-8')
        #     item["exchange"] = "sh".encode('utf-8')
        #     yield item

        # contsz=sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')[1].extract()
        # for stockSZ in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>',contsz):
        #     item["stockName"] = stockSZ.split("(")[0].encode('utf-8')
        #     item["stockCode"]=(stockSZ.split("(")[1][:-1]).encode('utf-8')
        #     item["exchange"] = "sz".encode('utf-8')
        #     yield item
    def parsecontent(self, response):

        def add1(matched):
            current_pagenum = int(matched.group("match")[1:-1]) + 1
            return "_%d." % current_pagenum

        sel = Selector(response)
        posts = sel.xpath('//*[@id="articlelistnew"]/div[@class="articleh"]')

        #below content is used to test the single page
        post = posts[0]
        title = post.xpath('.//span[@class="l3"]/a/@href').extract_first()
        post_page = self.site_domain + title
        logger.warning(post_page)
        yield Request(post_page, callback=self.parsepost)

        #below are used to get next pages
        # if len(posts) > 0:
            # current_url = response.url
            # next_page = re.sub(r'(?P<match>_\d+.)', add1, current_url)
            # for post in posts:
            #     title = post.xpath('.//span[@class="l3"]/a/@href').extract()[0]
            #     logger.warning(title)
            # yield Request(next_page, callback=self.parsecontent)

    def parsepost(self, response):
        logger.warning(response.url)
        sel = Selector(response)
        post_title = sel.xpath('//*[@id="zwconttbt"]/text()').extract_first().strip()
        logger.warning('post_title: %s' % post_title)


