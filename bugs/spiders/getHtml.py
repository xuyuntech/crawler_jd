# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from bugs.items import BugsItem

class GethtmlSpider(scrapy.Spider):
    name = 'getHtml'
    allowed_domains = ['www.jd.com']
    url = 'https://search.jd.com/Search?keyword=%E7%B2%BE%E6%B2%B9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%B2%BE%E6%B2%B9&psort=3&stock=1&page={page}&s=61&click=0'
    index = 1
    page = 20
    index_num = 2 * page
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               'Referer': 'https://search.jd.com'
               }

    # start_urls = ['http://www.jd.com/']
    def start_requests(self):
        url = self.url.format(page=self.index)
        yield Request(url, callback=self.parse, dont_filter=True)
        pass

    def parse(self, response):
        goos_id_topirty = []
        ids = response.xpath('//*[@id="J_goodsList"]/ul/li/@data-sku').extract()
        item = BugsItem()
        for id in ids:
            item['key'] = 'i'
            item['goods_id'] = id
            goos_id_topirty.append(id)
            yield item
            # print(self.index)
        self.index += 1
        url = 'https://search.jd.com/s_new.php?keyword=%E7%B2%BE%E6%B2%B9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.rem.0.V09&wq=%E7%B2%BE%E6%B2%B9&psort=3&stock=1&page={page}&s=31&scrolling=y&log_id=1524571725.40460&tpl=1_M&show_items='.format(
            page=self.index)
        for id in goos_id_topirty:
            url = url + str(id) + ','
        yield Request(url, callback=self.get_next, dont_filter=True, headers=self.headers)

    def get_next(self, response):
        ids = response.xpath('//li/@data-sku').extract()
        item = BugsItem()
        for id in ids:
            item['key'] = 'i'
            item['goods_id'] = id
            yield item
        if self.index < self.index_num:
            # print(self.index)
            self.index += 1
            url = self.url.format(page=self.index)
            yield Request(url, callback=self.parse, dont_filter=True)
