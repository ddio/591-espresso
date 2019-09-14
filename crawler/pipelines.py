import json
from scrapy_twrh.items import RawHouseItem, GenericHouseItem
from management.model import House

class DatabaseExporter(object):
    def process_item(self, item, spider):
        if isinstance(item, RawHouseItem):    
            house, created = House.get_or_create(
                job_id=spider.job.id,
                house_id=item['house_id']
            )
            if item['is_list']:
                house.list_meta = json.loads(item['raw'])
            elif 'dict' in item:
                house.detail_meta = item['dict']
            house.save()
        elif isinstance(item, GenericHouseItem) and 'rough_coordinate' in item:
            house, created = House.get_or_create(
                job_id=spider.job.id,
                house_id=item['vendor_house_id']
            )
            house.rough_gps = item['rough_coordinate']
            house.save()
        return item
