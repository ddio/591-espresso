from importlib import import_module
from types import ModuleType
from scrapy.crawler import CrawlerProcess
from crawler.spiders.oneshot_spider import OneshotSpider
from .subcmd import SubCmd
from .model import Job

class CrawlCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('crawl', help='Initiate a new crawler job')
        self.parser.add_argument(
            'url',
            help='Search url of target category. Should be sth like https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1'
        )
        self.parser.add_argument(
            '--cities',
            '-c',
            help='Comma separated list of city to crawl, use `台` instead of `臺`'
        )

    def get_crawler_settings(self):
        mod = import_module('crawler.settings')
        settings = {}
        for (name, item) in mod.__dict__.items():
            if not isinstance(item, ModuleType) and not name.startswith('__'):
                settings[name] = item
        return settings

    def execute(self, args):
        cities = []
        if args.cities:
            cities = args.cities.split(',')

        new_job = Job(url=args.url, cities=cities)
        new_job.save()

        settings = self.get_crawler_settings()

        crawler = CrawlerProcess(settings=settings)
        crawler.crawl(OneshotSpider, job_id=new_job.id)
        crawler.start()
