from scrapy import Spider
from scrapy import Selector
from scrapy import Request
from stocks.items import stockItem, userItem, postItem, commentItem
import parseUtils as utils
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

        yield Request(url, callback=self.parseContent)


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
    def parseContent(self, response):

        def add1(matched):
            current_pagenum = int(matched.group("match")) + 1
            return "%d" % current_pagenum

        sel = Selector(response)
        posts = sel.xpath('//*[@id="articlelistnew"]/div[@class="articleh"]')

        #below content is used to test the single page
        post = posts[5]
        title = post.xpath('.//span[@class="l3"]/a/@href').extract_first()
        post_page = self.site_domain + title
        post_page = utils.addPageForUrl(post_page)
        logger.warning(post_page)
        yield Request(post_page, callback=self.parsePost)

        #below are used to get next pages
        # if len(posts) > 0:
            # current_url = response.url
            # next_page = re.sub(r'_(?P<match>\d+)[.]', add1, current_url)
            # for post in posts:
            #     title = post.xpath('.//span[@class="l3"]/a/@href').extract()[0]
            #     logger.warning(title)
            # yield Request(next_page, callback=self.parseContent)

    def parsePost(self, response):
        sel = Selector(response)
        [stockId, postId] = utils.getIDSfromUrl(response.url)
        postSel = sel.xpath('//*[@id="zwcontent"]')
        if postSel.extract_first() is not None:
            postUserSel = postSel.xpath('.//*[@id="zwconttbn"]/strong/a')
            item_post = postItem()
            if postUserSel.extract_first() is not None:
                item_user = userItem()
                item_user["userName"] = postUserSel.xpath('.//text()').extract_first().strip()
                item_user["userId"] = postUserSel.xpath('.//@data-popper').extract_first().strip()
                item_post["userId"] = item_user["userId"]
                yield item_user

            item_post["stockId"] = stockId
            item_post["postId"] = postId
            item_post["title"] = postSel.xpath('.//*[@id="zwconttbt"]/text()').extract_first().strip()
            postTimeText = sel.xpath('.//*[@id="zwconttb"]/div[@class="zwfbtime"]/text()').extract_first()
            item_post["postTime"] = utils.getTimefromText(postTimeText)
            contents = sel.xpath('//*[@id="zwconbody"]//text()').extract()
            contents = [content.strip() for content in contents]
            item_post["content"] = '\n'.join(contents)
            item_post["forwardCount"] = sel.xpath('//*[@id="zfnums"]/text()').extract_first()
            if item_post["forwardCount"] is None:
                item_post["forwardCount"] = 0
            yield item_post

        commentsListSel = sel.xpath('//*[@id="zwlist"]/div[@class="zwli clearfix"]')
        for commentSel in commentsListSel:
            item_comment = commentItem()
            commentUserSel = commentSel.xpath('.//span[@class="zwnick"]/a')
            if commentUserSel.extract_first() is not None:
                item_user = userItem()
                item_user["userName"] = commentUserSel.xpath('.//text()').extract_first().strip()
                item_user["userId"] = commentUserSel.xpath('.//@data-popper').extract_first().strip()
                item_comment["userId"] = item_user["userId"]
                yield item_user
            item_comment["stockId"] = stockId
            item_comment["postId"] = postId
            commentTime = commentSel.xpath('.//div[@class="zwlitime"]/text()').extract_first()
            item_comment["commentTime"] = utils.getTimefromText(commentTime)
            item_comment["content"] = commentSel.xpath('.//div[@class="zwlitext stockcodec"]/text()').extract_first()
            item_comment["commentId"] = commentSel.xpath('.//@data-huifuid').extract_first()
            logging.warning(item_comment["stockId"])
            logging.warning(item_comment["postId"])
            logging.warning(item_comment["commentTime"])
            logging.warning(item_comment["content"])
            logging.warning(item_comment["commentId"])
            logging.warning(item_comment["userId"])
            yield item_comment
        #     relatedCommentSel = commentSel.xpath('.//div[@class="zwlitalkbox"]')
        #     if relatedCommentSel.extract_first() is not None:
        #         relatedCommentTimeText = relatedCommentSel.xpath('.//div[@class="zwlitalkboxtime"]').extract_first()
        #         relatedCommentTime = utils.getTimefromText(relatedCommentTimeText)
        #         logging.warning('relatedCommentTime: %s' % relatedCommentTime)
        #         relatedUserId = relatedCommentSel.xpath('.//div[@class="zwlitalkboxuinfo"]//span/@data-uid').extract_first()
        #         logging.warning('relatedUserId: %s' % relatedUserId)


