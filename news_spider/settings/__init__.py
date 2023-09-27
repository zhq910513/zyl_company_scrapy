BOT_NAME = 'news_search'

SPIDER_MODULES = ['news_spider.spiders']
NEWSPIDER_MODULE = 'news_spider.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_FAIL_ON_DATALOSS = False

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {}

# -----------------------------------------------------------------------------
# MIDDLEWARES, EXTENSIONS, PIPELINES
# -----------------------------------------------------------------------------

DOWNLOAD_TIMEOUT = 60

DOWNLOADER_MIDDLEWARES = {}

EXTENSIONS = {}

ITEM_PIPELINES = {}

SPIDER_MIDDLEWARES = {}

MONGODB_PORT = 27017

# 生产环境
MONGODB_HOST = '127.0.0.1'
# MONGODB_HOST = '27.150.182.135'
# MONGODB_USERNAME = None
# MONGODB_PASSWORD = None
MONGODB_USERNAME = 'readWrite'
MONGODB_PASSWORD = 'readWrite123456'

MONGODB_DATABASE = 'zyl_company_scrapy'
MONGODB_WEBSITE_COLLECTION = 'website'
MONGODB_URL_COLLECTION = 'urls'

MONGODB_URI = 'mongodb://{usr}:{pwd}@{host}:27017/{db}'
