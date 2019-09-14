# shared setting across different environment
# can be override by settings
import sys
import os
import scrapy
import logging

# scrapy.utils.log.configure_logging(install_root_handler=False)
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '../data/scrapy.log'),
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)

LOG_LEVEL = logging.INFO

BOT_NAME = os.environ.get('SCRAPY_BOT_NAME', 'dev-591-espresso-crawler')

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Need to be aware of meta redirect to avoid unnecessary download
METAREFRESH_ENABLED = False

# cookiejar are sometimes too smart....
COOKIES_ENABLED = False

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawler.pipelines.DatabaseExporter': 300
}

EXTENSIONS = {
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

DOWNLOAD_DELAY = 1
