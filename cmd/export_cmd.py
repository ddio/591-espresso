from .subcmd import SubCmd

class ExportCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('export', help='Export data in specified job')
        self.parser.add_argument(
            'id',
            help='ID of crawler job'
        )
        self.parser.add_argument(
            '--outfile',
            '-o',
            help='Name of output file'
        )

    def execute(self, args):
        raise NotImplementedError()
