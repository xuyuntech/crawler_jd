from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner(get_project_settings())
from bugs.spiders.getHtml import GethtmlSpider


d = runner.crawl(GethtmlSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()