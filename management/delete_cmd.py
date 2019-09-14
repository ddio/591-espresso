from .subcmd import SubCmd

class DeleteCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('delete', help='Delete specified job and its data')
        self.parser.add_argument(
            'id',
            help='ID of crawler job'
        )

    def execute(self, args):
        raise NotImplementedError()
