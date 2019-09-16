import yaml
from os import path, makedirs
import time
import csv
import logging
import json
from scrapy_twrh.spiders.util import clean_number
from .subcmd import SubCmd
from .model import House

class ExportCmd(SubCmd):
    def add_parser(self, subparser):
        self.parser = subparser.add_parser('export', help='Export data in specified job')
        self.parser.add_argument(
            'id',
            help='ID of crawler job'
        )
        self.parser.add_argument(
            'columns',
            help='column config file, see config/店面.yaml for example usage'
        )
        self.parser.add_argument(
            '--outfile',
            '-o',
            help='Name of output file, default data/<job_id>-<timestamp>.csv'
        )
        self.parser.add_argument(
            '--outprefix',
            '-p',
            help='''Export data of each city to a single file.
        File name would be <prefix>-<city name>.csv.
        <prefix> would be <job_id>-<timestamp> if only dir is given.'''
        )

    def get_default_prefix(self):
        now = time.strftime('%Y%m%d-%H%M%S')
        return f'{self.job_id}-{now}'

    def export_per_city(self, city_prefix):
        base_dir = path.dirname(city_prefix)
        base_prefix = path.basename(city_prefix)
        if not path.isdir(base_dir):
            makedirs(base_dir)

        if not base_prefix:
            base_prefix = self.get_default_prefix()

        opened_cities = {}

        for house in House.select().where(House.job_id == self.job_id):
            row = self.get_export_row_value(house)
            city = ''
            if house.detail_meta:
                city = house.detail_meta.get('top_region', '')

            if not city and house.list_meta:
                city = house.list_meta.get('region_name', '')

            if not opened_cities.get(city):
                city_path = path.join(base_dir, f'{base_prefix}-{city}.csv')
                opened_cities[city] = csv.writer(open(city_path, 'w'))
                self.print_header(opened_cities[city])

            opened_cities[city].writerow(row)

    def export_whole_job(self, outfile):
        if not outfile:
            outfile = path.join(
                path.dirname(__file__),
                f'../data/{self.get_default_prefix()}.csv'
            )
        with open(outfile, 'w') as csvfile:
            writer = csv.writer(csvfile)
            self.print_header(writer)

            for house in House.select().where(House.job_id == self.job_id):
                row = self.get_export_row_value(house)
                writer.writerow(row)

    def normalize_column_config(self, a_column, column_path):
        if isinstance(a_column, str):
            return {
                'label': a_column,
                'path': column_path
            }
        elif a_column.get('label'):
            return {
                **a_column,
                'path': column_path
            }
        else:
            return {
                **a_column,
                'label': '-'.join(column_path),
                'path': column_path
            }

    def expand_columns(self, to_expands):
        expanded_dict = {}
        for key in to_expands:
            expanded_dict[key] = {}

        for house in House.select().where(House.job_id == self.job_id):
            if house.detail_meta:
                for key in to_expands:
                    expanded_dict[key] = {
                        **expanded_dict[key],
                        **house.detail_meta.get(key, {})
                    }

        column_list = []
        for key in expanded_dict:
            for subkey in expanded_dict[key]:
                column_list.append(self.normalize_column_config(
                    {},
                    ['detail_meta', key, subkey]
                ))

        return column_list

    def gen_column_list(self, column_config):
        column_list = []
        need_expand = []

        def append_column_list(a_column, column_path):
            column_list.append(
                self.normalize_column_config(
                    a_column,
                    column_path
                )
            )

        if 'list_meta' in column_config:
            for key in column_config['list_meta']:
                append_column_list(
                    column_config['list_meta'][key],
                    ['list_meta', key]
                )
        if 'rough_gps' in column_config:
            append_column_list(
                column_config['rough_gps'],
                ['rough_gps']
            )

        if 'detail_meta' in column_config:
            for key in column_config['detail_meta']:
                a_column = column_config['detail_meta'][key]
                if isinstance(a_column, dict):
                    if a_column.get('_all'):
                        need_expand.append(key)
                    else:
                        for subkey in a_column:
                            append_column_list(
                                a_column[subkey],
                                ['detail_meta', key, subkey]
                            )        
                else:
                    append_column_list(
                        a_column,
                        ['detail_meta', key]
                    )

        if need_expand:
            column_list.extend(self.expand_columns(need_expand))

        return column_list

    def merge_column_list(self, column_list):
        merged_list = []
        merged_dict = {}

        def gen_path_config(column_config):
            path_config = column_config.copy()
            path_config.pop('label')
            return path_config

        for column in column_list:
            name = column['label']
            if name in merged_dict:
                merged_dict[name]['targets'].append(gen_path_config(column))
            else:
                merged_dict[name] = {
                    'label': name,
                    'targets': [
                        gen_path_config(column)
                    ]
                }
                merged_list.append(merged_dict[name])

        return merged_list

    def print_header(self, writer):
        headers = map(lambda column: column['label'], self.column_list)
        writer.writerow(headers)

    def get_cell_value(self, house, column_config):
        for target_config in reversed(column_config['targets']):
            value = self.get_target_value(house, target_config)
            if value is not None:
                return value

        return None

    def get_target_value(self, house, target_config):
        the_path = target_config['path']
        section = the_path[0]
        child_path = the_path[1:]
        cursor = getattr(house, section)

        for step in child_path:
            if isinstance(cursor, dict) and cursor.get(step):
                cursor = cursor.get(step)
            else:
                cursor = None
                break

        if isinstance(cursor, dict):
            cursor = json.dumps(cursor, ensure_ascii=False)

        if target_config.get('clean_number'):
            cursor = clean_number(cursor)

        return cursor

    def get_export_row_value(self, row):
        return map(
            lambda column: self.get_cell_value(row, column),
            self.column_list
        )

    def execute(self, args):
        self.job_id = args.id

        if not path.isfile(args.columns):
            logging.error(f'Invalid column config: {args.columns}')
            return

        # prepare normalized column list
        column_config = {}
        with open(args.columns, 'r') as f:
            column_config = yaml.safe_load(f)

        self.column_list = self.merge_column_list(
            self.gen_column_list(column_config)
        )

        # export per city file?
        if args.outprefix:
            self.export_per_city(args.outprefix)
        else:
            self.export_whole_job(args.outfile)
