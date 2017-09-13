from scrapy import Spider
from scrapy import Selector
import re

class gubaSpider(Spider):
    name = 'guba'
    allowed_domain = ['eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html#sh/']

    def parse(self, response):
        sel = Selector(response)

        contsh=sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')[0].extract()
        for stockSH in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>',contsh):
            if (stockSH.split("(")[1][:-1]).encode('utf-8').startswith('20'):
                continue
            item["stockName"] = stockSH.split("(")[0].encode('utf-8')
            item["stockCode"]=(stockSH.split("(")[1][:-1]).encode('utf-8')
            item["exchange"] = "sh".encode('utf-8')
            yield item

        contsz=sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')[1].extract()
        for stockSZ in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>',contsz):
            item["stockName"] = stockSZ.split("(")[0].encode('utf-8')
            item["stockCode"]=(stockSZ.split("(")[1][:-1]).encode('utf-8')
            item["exchange"] = "sz".encode('utf-8')
            yield item
