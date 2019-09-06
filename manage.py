import argparse
import abc

class SubCmd(abc.ABC):
    @abc.abstractmethod
    def add_parser(self, subparser):
        return NotImplemented

    @abc.abstractmethod
    def execute(self, args):
        return NotImplemented

class ListCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('list', help='List all existing crawler jobs')

    def execute(self, args):
        raise NotImplementedError()

class CrawlCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('crawl', help='Initiate a new crawler job')
        self.parser.add_argument(
            'url',
            help='Search url of target category. Should be sth like https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1'
        )

    def execute(self, args):
        raise NotImplementedError()

class EspressoCmd():
    cmds = dict(
        list=ListCmd(),
        crawl=CrawlCmd()
    )
    def __init__(self):
        parser = argparse.ArgumentParser(description='Crawl and export 591 data once')
        subparsers = parser.add_subparsers(title='subcommands', dest='cmd')
        for cmd in self.cmds:
            self.cmds[cmd].add_parser(subparsers)

        args = parser.parse_args()

        if args.cmd not in self.cmds:
            parser.print_help()
            exit(1)
        
        self.cmds[args.cmd].execute(args)

if __name__ == '__main__':
    EspressoCmd()
