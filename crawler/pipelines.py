import json
from scrapy_twrh.items import RawHouseItem, GenericHouseItem
from management.model import House, HouseStats

class DatabaseExporter(object):
    def process_item(self, item, spider):
        if isinstance(item, RawHouseItem):    
            house = House.get_or_create(
                job_id=spider.job.id,
                house_id=item['house_id']
            )[0]

            stats = HouseStats.get_or_create(
                job_id=spider.job.id,
                house_id=item['house_id']
            )[0]

            if item['is_list']:
                house.list_meta = json.loads(item['raw'])
                stats.list_count += 1
                stats.is_vip = 'id' not in house.list_meta
            elif 'dict' in item:
                house.detail_meta = item['dict']
                stats.detail_count += 1
            house.save()
            stats.save()
        elif isinstance(item, GenericHouseItem) and 'rough_coordinate' in item:
            house = House.get_or_create(
                job_id=spider.job.id,
                house_id=item['vendor_house_id']
            )[0]

            stats = HouseStats.get_or_create(
                job_id=spider.job.id,
                house_id=item['vendor_house_id']
            )[0]

            gps = item['rough_coordinate']
            house.rough_gps = [gps[0].__str__(), gps[1].__str__()]
            house.save()
            stats.gps_count += 1
            stats.save()
        return item
