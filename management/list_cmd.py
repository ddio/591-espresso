from .subcmd import SubCmd
from .model import Job, House

class ListCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('list', help='List all existing crawler jobs')

    def execute(self, args):
        print('ID | URL                       | Cities    | Opts           |  #House')
        print('---------------------------------------------------------------------')
        for job in Job.select().order_by(Job.created_at.desc()):
            count = job.houses.count()
            cities = '*'
            if job.cities:
                cities = ', '.join(job.cities)
            print(f'{job.id} | {job.url} | {cities} | {job.opts} | {count}')
