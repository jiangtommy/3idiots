from scrapy import Spider
from scrapy import Selector
from stocks.items import StocksItem
import re

class DfcfSpider(Spider):
    name = 'dfcf'
    allowed_domain = ['eastmoney.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html#sh/']

    def parse(self, response):
        sel = Selector(response)
        item = StocksItem()

        contsh=sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')[0].extract()
        for stockSH in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>',contsh):
            item["stockName"] = stockSH.split("(")[0].encode('utf-8')
            item["stockCode"]=("sh"+stockSH.split("(")[1][:-1]).encode('utf-8')
            yield item

        contsz=sel.xpath('//div[@class="qox"]/div[@class="quotebody"]/div/ul')[1].extract()
        for stockSZ in re.findall(r'<li>.*?<a.*?target=.*?>(.*?)</a>',contsz):
            item["stockName"] = stockSZ.split("(")[0].encode('utf-8')
            item["stockCode"]=("sz"+stockSZ.split("(")[1][:-1]).encode('utf-8')
            yield item
