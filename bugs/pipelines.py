# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import copy
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import elasticsearch.helpers
from bugs import settings


class BugsPipeline(object):
    def open_spider(self, spider):
        self.ids = []
    def close_spider(self, spider):
        self.file.close()


    def process_item(self, item, spider):

        if item['key'] == 'i':
            if item['goods_id'] in self.ids:
                return item
            else:
                self.name = './data/jd-goods-id.json'
                self.file = codecs.open(filename=self.name, mode='a', encoding='utf-8')
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.file.write(line)
                self.ids.append(item['goods_id'])
                # print(self.ids)
                return item
        if item['key'] == 'c':
            self.name = './data/jd-'+ str(item['goods_id'])+'-comment.json'
            self.file = codecs.open(filename=self.name, mode='a', encoding='utf-8')
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            return item
        if item['key'] == 'd':
            self.name = './data/jd-goods-detail.json'
            self.file = codecs.open(filename=self.name, mode='a', encoding='utf-8')
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            return item
class ELKPipeline(object):

    def open_spider(self, spider):
        self.es = Elasticsearch(settings.addr)

    def close_spider(self, spider):
        pass



    def process_item(self, asynItem, spider):
        asynItem = copy.deepcopy(asynItem)
        if asynItem['key'] == 'i':
            pass
        if asynItem['key'] == 'c':
            if 'comment_content' in asynItem :
                action = [{
                    "_index": settings.index,
                    "_type": settings.type,
                    "_source": {"key":asynItem['key'],
                        "goods_id": asynItem['goods_id'],
                        "goods_name": asynItem['goods_name'],
                        "comment_id": asynItem['comment_id'],
                        "comment_index": asynItem['comment_index'],
                        "comment_content": asynItem['comment_content'],
                        "comment_time": asynItem['comment_time']}
                }]
                elasticsearch.helpers.bulk(self.es, action)
                # self.actions.append(action)
            #     data = {"key":item['key'],
            #             "goods_id": item['goods_id'],
            #             "goods_name": item['goods_name'],
            #             "comment_id": item['comment_id'],
            #             "comment_index": item['comment_index'],
            #             "comment_content": item['comment_content'],
            #             "comment_time": item['comment_time']}
            # # self.name = str(item['goods_id']) + '-comment'
            #     self.es.index(index="jd", doc_type="JD", body=data)
                return asynItem
            elif 'good_content' in asynItem:
                action = [{
                    "_index": settings.index,
                    "_type": settings.type,
                    "_source": {"key": asynItem['key'],
                        "goods_id": asynItem['goods_id'],
                        "goods_name": asynItem['goods_name'],
                        "comment_id": asynItem['comment_id'],
                        "comment_index": asynItem['comment_index'],
                        "good_content": asynItem['good_content'],
                        "comment_time": asynItem['comment_time']}
                }]
                elasticsearch.helpers.bulk(self.es, action)
                # self.actions.append(action)

                # data = {"key": item['key'],
                #         "goods_id": item['goods_id'],
                #         "goods_name": item['goods_name'],
                #         "comment_id": item['comment_id'],
                #         "comment_index": item['comment_index'],
                #         "good_content": item['good_content'],
                #         "comment_time": item['comment_time']}
                # # self.name = str(item['goods_id']) + '-comment'
                # self.es.index(index="jd", doc_type="JD", body=data)
                return asynItem
            elif 'general_content' in asynItem:
                action = [{
                    "_index": settings.index,
                    "_type": settings.type,
                    "_source": {"key": asynItem['key'],
                        "goods_id": asynItem['goods_id'],
                        "goods_name": asynItem['goods_name'],
                        "comment_id": asynItem['comment_id'],
                        "comment_index": asynItem['comment_index'],
                        "general_content": asynItem['general_content'],
                        "comment_time": asynItem['comment_time']}
                }]
                elasticsearch.helpers.bulk(self.es, action)
                # self.actions.append(action)
                # data = {"key": item['key'],
                #         "goods_id": item['goods_id'],
                #         "goods_name": item['goods_name'],
                #         "comment_id": item['comment_id'],
                #         "comment_index": item['comment_index'],
                #         "general_content": item['general_content'],
                #         "comment_time": item['comment_time']}
                # # self.name = str(item['goods_id']) + '-comment'
                # self.es.index(index="jd", doc_type="JD", body=data)
                return asynItem
            else:
                action = [{
                    "_index": settings.index,
                    "_type": settings.type,
                    "_source": {"key": asynItem['key'],
                        "goods_id": asynItem['goods_id'],
                        "goods_name": asynItem['goods_name'],
                        "comment_id": asynItem['comment_id'],
                        "comment_index": asynItem['comment_index'],
                        "poor_content": asynItem['poor_content'],
                        "comment_time": asynItem['comment_time']}
                }]
                elasticsearch.helpers.bulk(self.es, action)
                # self.actions.append(action)
                # data = {"key": item['key'],
                #         "goods_id": item['goods_id'],
                #         "goods_name": item['goods_name'],
                #         "comment_id": item['comment_id'],
                #         "comment_index": item['comment_index'],
                #         "poor_content": item['poor_content'],
                #         "comment_time": item['comment_time']}
                # # self.name = str(item['goods_id']) + '-comment'
                # self.es.index(index="jd", doc_type="JD", body=data)
                return asynItem

        if asynItem['key'] == 'd':
            action = [{
                "_index": settings.index,
                "_type": settings.type,
                "_source": {"key":asynItem['key'],
                    "goods_id": asynItem['goods_id'],
                    "shop_name": asynItem['shop_name'],
                    "goods_name": asynItem['goods_name'],
                    "CommentCount": asynItem['CommentCount'],
                    "GoodCount": asynItem['GoodCount'],
                    "GoodRate": asynItem['GoodRate'],
                    "GeneralCount": asynItem['GeneralCount'],
                    "GeneralRate": asynItem['GeneralRate'],
                    "PoorCount": asynItem['PoorCount'],
                    "PoorRate": asynItem['PoorRate'],
                    "DefaultGoodCount": asynItem['DefaultGoodCount'],
                    "price": asynItem['price'],
                    "@datatime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")
                }
            }]
            elasticsearch.helpers.bulk(self.es, action)
            # self.actions.append(action)

            # data = {"key":item['key'],
            #         "goods_id": item['goods_id'],
            #         "shop_name": item['shop_name'],
            #         "goods_name": item['goods_name'],
            #         "CommentCount": item['CommentCount'],
            #         "GoodCount": item['GoodCount'],
            #         "GoodRate": item['GoodRate'],
            #         "GeneralCount": item['GeneralCount'],
            #         "GeneralRate": item['GeneralRate'],
            #         "PoorCount": item['PoorCount'],
            #         "PoorRate": item['PoorRate'],
            #         "DefaultGoodCount": item['DefaultGoodCount'],
            #         "price": item['price'],
            #         "@datatime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")
            #     }
            # self.es.index(index="jd", doc_type="JD", body=data)
            return asynItem


