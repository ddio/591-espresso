from .subcmd import SubCmd

class ResumeCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('resume', help='Resume a previously stopped job')
        self.parser.add_argument(
            'id',
            help='ID of crawler job'
        )

    def execute(self, args):
        raise NotImplementedError()
