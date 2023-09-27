from . import ITEM_PIPELINES, DOWNLOADER_MIDDLEWARES

# -----------------------------------------------------------------------------
# ASYNC PIPELINE MONGODB
# -----------------------------------------------------------------------------

ITEM_PIPELINES.update({
    'scrapy_pipeline_mongodb.pipelines.mongodb_async.PipelineMongoDBAsync': 100,
})

DOWNLOADER_MIDDLEWARES.update({
    'news_spider.downloadermiddlewares.web_chrome.SeleniumMiddleware': 550,
    'news_spider.downloadermiddlewares.url_mark.UrlsMarkDownloaderMiddleware': 600,
})

# 设置ChromeDriver的执行path
# CHROME_DRIVER_PATH = r"C:\Users\king\AppData\Local\Programs\Python\Python39\chromedriver.exe"
CHROME_DRIVER_PATH = r"/usr/local/python3/bin/chromedriver.exe"

MONGODB_HOST = '127.0.0.1'
# MONGODB_HOST = '27.150.182.135'
MONGODB_PORT = 27017

# MONGODB_USERNAME = None
# MONGODB_PASSWORD = None
MONGODB_USERNAME = 'readWrite'
MONGODB_PASSWORD = 'readWrite123456'

MONGODB_DATABASE = 'zyl_company_scrapy'
MONGODB_COLLECTION = 'urls'

# used settings.set() when start to spider

MONGODB_INDEXES = [
    # ('company_url', ASCENDING, {}),
    # ('source_url', ASCENDING, {}),
]

MONGODB_PROCESS_ITEM = 'news_spider.pipelines.insert_pipeline.process_item'
