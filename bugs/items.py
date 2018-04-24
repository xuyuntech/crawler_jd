# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BugsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    key = scrapy.Field()
    CommentCount = scrapy.Field()
    GoodCount =scrapy.Field()
    GoodRate = scrapy.Field()
    GeneralCount = scrapy.Field()
    GeneralRate = scrapy.Field()
    PoorCount = scrapy.Field()
    PoorRate = scrapy.Field()
    DefaultGoodCount = scrapy.Field()
    price = scrapy.Field()
    shop_name = scrapy.Field()
    goods_id = scrapy.Field()
    goods_name = scrapy.Field()
    comment_id = scrapy.Field()
    comment_index = scrapy.Field()
    comment_content = scrapy.Field()
    comment_time = scrapy.Field()
    good_content = scrapy.Field()
    general_content = scrapy.Field()
    poor_content = scrapy.Field()
    data_time = scrapy.Field()


