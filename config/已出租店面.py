from datetime import timedelta, datetime, timezone
from scrapy_twrh.spiders.util import clean_number
from management.model import House

taipei_time = timezone(timedelta(hours=8))

def parse_dealtime(row: House):
    base_time = row.created_at
    deal_days_ago = row.list_meta.get('addInfo')

    try:
        deal_days_ago = clean_number(deal_days_ago)
    except ValueError:
        return None

    if deal_days_ago is None:
        return None

    base_time -= timedelta(days=deal_days_ago)
    return base_time.astimezone(taipei_time).strftime('%Y-%m-%d')

column_config = {
    'list_meta': {
        'houseid': '591編號',
        'post_id': '591編號',
        'region_name': '城市',
        'section_name': '鄉鎮市區',
        'section_str': '鄉鎮市區',
        'address': '自訂地址',
        'price': {
            'label': '租金',
            'clean_number': True
        },
        'area': {
            'label': '坪數',
            'clean_number': True
        },
        'posttime': '最後更新相對日期',
        'addInfo': {
            'label': '成交於幾天前',
            'clean_number': True
        },
        'dealtime': {
            'label': '成交日期',
            'fn': parse_dealtime
        }
    },
    'detail_meta': {
        'n_views': '瀏覽次數',
        'address': '完整地址',
        'top_region': '城市',
        'sub_region': '鄉鎮市區',
        'title': '標題',
        'imgs': '照片',
        'top_metas': {
            '_all': True
        },
        'side_metas': {
            '_all': True
        },
        'environment': {
            '_all': True
        },
        'is_deal': '已成交',
        'owner': {
            '_all': True
        },
        'desp': '說明'
    },
    'rough_gps': '約略座標'
}