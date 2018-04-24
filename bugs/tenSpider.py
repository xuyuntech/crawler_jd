from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import json
# 加入项目配置文件
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
reactor.suggestThreadPoolSize(30)
runner = CrawlerRunner(get_project_settings())
# 导入爬虫
from bugs.spiders.jd_spider import JDSpoder
# urls = []
# for line in open('../data/jd-goods-id.json', 'r',encoding="utf8"):
#     data = json.loads(line)
#     url = 'https://item.jd.com/{id}.html'.format(id = data['goods_id'])
#     urls.append(url)
# 'https://item.jd.com/14786160283.html',
urls = ['https://item.yiyaojd.com/13674344768.html',
        'https://item.yiyaojd.com/3154005.html',
        'https://item.yiyaojd.com/4410004.html',
        'https://item.yiyaojd.com/13214528412.html',
        'https://item.yiyaojd.com/4808847.html',
        'https://item.yiyaojd.com/3091800.html',
        'https://item.yiyaojd.com/3108320.html',
        'https://item.yiyaojd.com/12801590412.html',
        'https://item.yiyaojd.com/3172871.html',
        'https://item.yiyaojd.com/17990313602.html']
for i in range(len(urls)):
    kwargs = {'url': '{}'.format(urls[i])}
    runner.crawl(JDSpoder, **kwargs)
# # 返回所有托管crawlers完成执行时触发的延迟。
d =  runner.join()
# 关闭reactor
d.addBoth(lambda _: reactor.stop())
reactor.run()
