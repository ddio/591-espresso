import argparse
from management import ListCmd, CrawlCmd, ResumeCmd, ExportCmd, DeleteCmd

class EspressoCmd():
    cmds = dict(
        list=ListCmd(),
        crawl=CrawlCmd(),
        resume=ResumeCmd(),
        delete=DeleteCmd(),
        export=ExportCmd()
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
