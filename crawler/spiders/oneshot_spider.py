""" Crawl 591 one time

```
scrapy crawl oneshot -a job_id=1
```
"""
import json
import logging
from peewee import DoesNotExist
from scrapy import Request
from scrapy_twrh.spiders.util import clean_number
from scrapy_twrh.spiders.enums import UNKNOWN_ENUM
from scrapy_twrh.spiders.rental591 import Rental591Spider, util
from scrapy_twrh.items import RawHouseItem, GenericHouseItem
from management.model import Job

class OneshotSpider(Rental591Spider):
    name = 'oneshot'

    def __init__(self, job_id, novip):
        try:
            job_id = int(job_id)
        except ValueError:
            logging.error(f'Invalid Job ID: {job_id}')
            raise ValueError

        try:
            job = Job.get(Job.id == job_id)
        except DoesNotExist:
            logging.error(f'Job ID {job_id} not found')
            raise DoesNotExist

        self.job = job
        self.novip = novip

        args = {}

        if job.cities:
            args['target_cities'] = job.cities

        super().__init__(
            **args,
            parse_list=self.count_and_parse_list
        )

    def count_and_parse_list(self, response):
        meta = response.meta['rental']
        data = json.loads(response.text)

        if meta.page == 0:
            count = clean_number(data['records'])
            logging.info(f'[{meta.name}] total {count} house to crawl!')

            # #items return per request may differ from API endpoint
            self.N_PAGE = len(data['data']['data'])

            # generate all list request as now we know number of result
            cur_page = 1
            while cur_page * self.N_PAGE < count:
                yield self.gen_list_request(util.ListRequestMeta(
                    meta.id,
                    meta.name,
                    cur_page
                ))
                cur_page += 1

        
        houses = data['data']['data']

        if not self.novip:
            houses = data['data']['topData'] + houses

        for house in houses:
            # copy from twrh
            house['is_vip'] = 'id' not in house
            house_item = self.gen_shared_attrs(house, meta)
            yield RawHouseItem(
                house_id=house_item['vendor_house_id'],
                vendor=self.vendor,
                is_list=True,
                raw=json.dumps(house, ensure_ascii=False)
            )
            yield GenericHouseItem(**house_item)
            yield self.gen_detail_request(
                util.DetailRequestMeta(house_item['vendor_house_id'], False)
            )

    def get_enum(self, enum_cls, house_id, value):
        # ignore undefined enum as we are collecting generic rental item
        try:
            enum = enum_cls[value]
        except KeyError:
            enum = UNKNOWN_ENUM

        return enum

    def gen_list_request_args(self, rental_meta: util.ListRequestMeta):
        """add order and orderType, so to get latest created house"""
        url = f'{self.job.url}&region={rental_meta.id}&firstRow={rental_meta.page * self.N_PAGE}'
        
        return {
            **super().gen_list_request_args(rental_meta),
            'url': url
        }
