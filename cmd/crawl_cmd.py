from .subcmd import SubCmd

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

    def execute(self, args):
        raise NotImplementedError()
