import scrapy
import json
import re
from datetime import datetime
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from bugs.items import BugsItem
import time



class JDSpoder(scrapy.Spider):
    name = 'jd'
    goods_type = []
    index = 1
    CommentCount = 1
    GoodCount = 1
    GeneralCount = 1
    PoorCount = 1
    def __init__(self,**kwargs):
        super(JDSpoder, self).__init__(**kwargs)
        # print(args)
        self.start_urls = [kwargs.get('url')]
        self.url_num = 0
        self.data = BugsItem()
        self.gid = '0'
    def parse(self, response):
        self.gid = response.url.split('/')[-1].strip('.html')
        selected = []
        self.data['key'] = 'd'
        self.data['goods_id'] = str(self.gid)
        self.data['shop_name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[2]/div/div[1]/div/a/text()').extract_first()
        # try:
        #     mid1 = response.xpath('/html/body/div[5]/div/div[2]/div[1]/text()').extract()
        #     mid2 = mid1[1].replace(" ", '')
        #     mid3 = mid2.replace("\n", '')
        #     self.data['goods_name'] = mid3
        # except Exception as e:
        #     self.data['goods_name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[9]/text()').extract_first()
        self.data['goods_name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[9]/text()').extract_first()
        # self.data['goods_name'] = response.xpath('//*[@id="detail"]/div[2]/div[2]/div[1]/div/dl/dd[3]/text()').extract_first()

        try:
            selected = response.xpath('//*[@id="choose-attr-1"]/div[2]/div/@class').extract()
            lo = selected.index('item  selected  ') + 1
            self.goods_type = response.xpath(
                '//*[@id="choose-attr-1"]/div[2]/div[' + str(lo) + ']/@data-value').extract()
        except Exception as e:
            pass
        url = 'http://club.jd.com/ProductPageService.aspx?method=GetCommentSummaryBySkuId&referenceId={}'.format(self.gid)
        yield Request(url,callback=self.comment_num,dont_filter=True)
    def comment_num(self,response):
        datas = json.loads(response.body)
        self.data['CommentCount'] = datas['CommentCount']
        self.data['GoodCount'] = datas['GoodCount']
        self.data['GoodRate'] = datas['GoodRate']
        self.data['GeneralCount'] = datas['GeneralCount']
        self.data['GeneralRate'] = datas['GeneralRate']
        self.data['PoorCount'] = datas['PoorCount']
        self.data['PoorRate'] = datas['PoorRate']
        self.data['DefaultGoodCount'] = datas['DefaultGoodCount']
        url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(self.gid)
        yield Request(url,callback=self.price,dont_filter=True)

    def price(self, response):
        datas = json.loads(response.body)
        datas = datas[0]
        self.data['price'] = datas['p']
        item = BugsItem()
        item['key'] = self.data['key']
        item['goods_id'] = self.data['goods_id']
        item['shop_name'] = self.data['shop_name']
        item['goods_name'] = self.data['goods_name']
        item['CommentCount'] = self.data['CommentCount']
        item['GoodCount'] = self.data['GoodCount']
        item['GoodRate'] = self.data['GoodRate']
        item['GeneralCount'] = self.data['GeneralCount']
        item['GeneralRate'] = self.data['GeneralRate']
        item['PoorCount'] = self.data['PoorCount']
        item['PoorRate'] = self.data['PoorRate']
        item['DefaultGoodCount'] = self.data['DefaultGoodCount']
        item['price'] =  self.data['price']
        item['data_time'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")
        yield item
        url = 'http://club.jd.com/review/{}-1-1-0.html'.format(self.gid)
        # yield Request(url,callback=self.comment,dont_filter=True)

    def comment(self, response):
        items = []
        comment_num = len(response.xpath('//*[@id="comments-list"]/div/@id').extract())-4
        for i in range(comment_num):
            try:
                if response.xpath('//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/div/dl/dd/text()').extract_first().replace("\r\n", '') == self.goods_type[0]:
                    item = BugsItem()
                    item['key'] = 'c'
                    item['goods_id'] = str(self.gid)
                    item['goods_name'] = self.data['goods_name']
                    item['comment_id'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                              '')
                    item['comment_index'] = str(self.CommentCount)
                    item['comment_content'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                    string = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                        "\r\n", '')
                    Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                    date = re.match(Regular_expression, string).group()
                    item['comment_time'] = date
                    items.append(item)
                    yield item
            except Exception as e:
                item = BugsItem()
                item['key'] = 'c'
                item['goods_id'] = str(self.gid)
                item['goods_name'] = self.data['goods_name']
                item['comment_id'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                          '')
                item['comment_index'] = str(self.CommentCount)
                item['comment_content'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                string = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                    "\r\n", '')
                Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                date = re.match(Regular_expression, string).group()
                item['comment_time'] = date
                items.append(item)
                yield item

        self.CommentCount += 1
        url = 'http://club.jd.com/review/{}-1-{}-0.html'.format(str(self.gid),str(self.CommentCount))
        time.sleep(5)
        if(self.CommentCount <= 2):
            yield Request(url, callback=self.comment,dont_filter=True)
        else:
            url = 'http://club.jd.com/review/{}-1-1-3.html'.format(str(self.gid))
            # yield Request(url, callback=self.good_comment,dont_filter=True)

    def good_comment(self, response):
        items = []
        comment_num = len(response.xpath('//*[@id="comments-list"]/div/@id').extract())-4
        for i in range(comment_num):
            try:
                if response.xpath('//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/div/dl/dd/text()').extract_first().replace("\r\n", '') == self.goods_type[0]:
                    item = BugsItem()
                    item['key'] = 'c'
                    item['goods_id'] = str(self.gid)
                    item['goods_name'] = self.data['goods_name']
                    item['comment_id'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                              '')
                    item['comment_index'] = str(self.GoodCount)
                    item['good_content'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                    string = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                        "\r\n", '')
                    Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                    date = re.match(Regular_expression, string).group()
                    item['comment_time'] = date
                    items.append(item)
                    yield item
            except Exception as e:
                item = BugsItem()
                item['key'] = 'c'
                item['goods_id'] = str(self.gid)
                item['goods_name'] = self.data['goods_name']
                item['comment_id'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                          '')
                item['comment_index'] = str(self.GoodCount)
                item['good_content'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                string = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                    "\r\n", '')
                Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                date = re.match(Regular_expression, string).group()
                item['comment_time'] = date
                items.append(item)
                yield item

        self.GoodCount += 1
        url = 'http://club.jd.com/review/{}-1-{}-3.html'.format(str(self.gid),str(self.GoodCount))
        time.sleep(5)
        if(self.GoodCount <= 2):
            yield Request(url, callback=self.good_comment,dont_filter=True)
        else:
            url = 'http://club.jd.com/review/{}-1-1-2.html'.format(str(self.gid))
            yield Request(url, callback=self.general_comment,dont_filter=True)
    def general_comment(self, response):
        items = []
        comment_num = len(response.xpath('//*[@id="comments-list"]/div/@id').extract())-4
        for i in range(comment_num):
            try:
                if response.xpath('//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/div/dl/dd/text()').extract_first().replace("\r\n", '') == self.goods_type[0]:
                    item = BugsItem()
                    item['key'] = 'c'
                    item['goods_id'] = str(self.gid)
                    item['goods_name'] = self.data['goods_name']
                    item['comment_id'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                              '')
                    item['comment_index'] = str(self.GeneralCount)
                    item['general_content'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                    string = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                        "\r\n", '')
                    Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                    date = re.match(Regular_expression, string).group()
                    item['comment_time'] = date
                    items.append(item)
                    yield item
            except Exception as e:
                item = BugsItem()
                item['key'] = 'c'
                item['goods_id'] = str(self.gid)
                item['goods_name'] = self.data['goods_name']
                item['comment_id'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                          '')
                item['comment_index'] = str(self.GeneralCount)
                item['general_content'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                string = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                    "\r\n", '')
                Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                date = re.match(Regular_expression, string).group()
                item['comment_time'] = date
                items.append(item)
                yield item

        self.GeneralCount += 1
        url = 'http://club.jd.com/review/{}-1-{}-2.html'.format(str(self.gid),str(self.GeneralCount))
        time.sleep(5)
        if(self.GeneralCount <= 2):
            yield Request(url, callback=self.general_comment,dont_filter=True)
        else:
            url = 'http://club.jd.com/review/{}-1-1-1.html'.format(str(self.gid))
            yield Request(url, callback=self.poor_comment,dont_filter=True)

    def poor_comment(self, response):
        items = []
        comment_num = len(response.xpath('//*[@id="comments-list"]/div/@id').extract())-4
        for i in range(comment_num):
            try:
                if response.xpath('//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/div/dl/dd/text()').extract_first().replace("\r\n", '') == self.goods_type[0]:
                    item = BugsItem()
                    item['key'] = 'c'
                    item['goods_id'] = str(self.gid)
                    item['goods_name'] = self.data['goods_name']
                    item['comment_id'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                              '')
                    item['comment_index'] = str(self.PoorCount)
                    item['poor_content'] = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                    string = response.xpath(
                        '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                        "\r\n", '')
                    Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                    date = re.match(Regular_expression, string).group()
                    item['comment_time'] = date
                    items.append(item)
                    yield item
            except Exception as e:
                item = BugsItem()
                item['key'] = 'c'
                item['goods_id'] = str(self.gid)
                item['goods_name'] = self.data['goods_name']
                item['comment_id'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[1]/div[2]/text()').extract_first().replace("\r\n",
                                                                                                          '')
                item['comment_index'] = str(self.PoorCount)
                item['poor_content'] = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[2]/dl/dd/text()').extract_first()
                string = response.xpath(
                    '//*[@id="comment-' + str(i) + '"]/div/div[2]/div[1]/span[2]/a/text()').extract_first().replace(
                    "\r\n", '')
                Regular_expression = '([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))'
                date = re.match(Regular_expression, string).group()
                item['comment_time'] = date
                items.append(item)
                yield item

        self.PoorCount += 1
        url = 'http://club.jd.com/review/{}-1-{}-1.html'.format(str(self.gid),str(self.PoorCount))
        time.sleep(5)
        if(self.PoorCount <= 2):
            yield Request(url, callback=self.poor_comment,dont_filter=True)