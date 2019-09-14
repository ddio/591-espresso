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
from scrapy_twrh.spiders.rental591 import Rental591Spider, util
from scrapy_twrh.items import RawHouseItem
from management.model import Job

class OneshotSpider(Rental591Spider):
    name = 'oneshot'

    def __init__(self, job_id):
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

        args = {}

        if job.cities:
            args['target_cities'] = job.cities

        super().__init__(
            **args,
            parse_list=self.count_and_parse_list
        )

    def count_and_parse_list(self, response):
        meta = response.meta['rental']

        if meta.page == 0:
            data = json.loads(response.text)
            count = clean_number(data['records'])
            logging.info(f'[{meta.name}] total {count} house to crawl!')

        for item in self.default_parse_list(response):
            yield item

    def gen_list_request_args(self, rental_meta: util.ListRequestMeta):
        """add order and orderType, so to get latest created house"""
        url = f'{self.job.url}&region={rental_meta.id}&firstRow={rental_meta.page}'
        
        return {
            **super().gen_list_request_args(rental_meta),
            'url': url
        }
