from . import DOWNLOADER_MIDDLEWARES
from . import SPIDER_MIDDLEWARES
from ..settings import *

# ------------------------------------------------------------------------------
# PROXY MANAGEMENT
# ------------------------------------------------------------------------------

DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy_proxy_management.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750
})

HTTPPROXY_ENABLED = True

# ------------------------------------------------------------------------------
# MongoDB Proxy Storage
# ------------------------------------------------------------------------------

HTTPPROXY_STORAGE = 'scrapy_proxy_management.storages.mongodb_storage.MongoDBSyncStorage'

HTTPPROXY_STRATEGY = 'scrapy_proxy_management.strategies.mongodb_strategy.MongoDBStrategy'

HTTPPROXY_MONGODB_HOST = MONGODB_HOST
HTTPPROXY_MONGODB_PORT = 27017

# HTTPPROXY_MONGODB_USERNAME = MONGODB_USERNAME
# HTTPPROXY_MONGODB_PASSWORD = MONGODB_PASSWORD

# HTTPPROXY_MONGODB_OPTIONS_ =

HTTPPROXY_MONGODB_DATABASE = HTTPPROXY_MONGODB_DATABASE
HTTPPROXY_MONGODB_AUTHSOURCE = HTTPPROXY_MONGODB_DATABASE

HTTPPROXY_MONGODB_COLLECTION = HTTPPROXY_MONGODB_COLLECTION

HTTPPROXY_MONGODB_PROXY_RETRIEVER = {
    'name': 'find',
    'filter': None,
    'projection': {
        '_id': 1, 'scheme': 1, 'ip': 1, 'port': 1, 'username': 1, 'password': 1
    },
    'skip': 0,
    'limit': 0,
    'sort': None
}

HTTPPROXY_MONGODB_GET_PROXY_FROM_DOC = 'scrapy_proxy_management.storages.mongodb_storage.get_proxy_from_doc_2'

# ------------------------------------------------------------------------------
# BLOCK INSPECTOR IN DOWNLOADER & SPIDER MIDDLEWARES
# ------------------------------------------------------------------------------

DOWNLOADER_MIDDLEWARES.update({
    # 'scrapy_proxy_management.downloadermiddlewares.block_inspector.BlockInspectorMiddleware': 751
})

SPIDER_MIDDLEWARES.update({
    # 'scrapy_proxy_management.spidermiddlewares.block_inspector.BlockInspectorMiddleware': 40
})

HTTPPROXY_PROXY_INVALIDATED_STATUS_CODES = {502, 503, 500, 400, 401, 402, 403, 404}
# HTTPPROXY_PROXY_DM_BLOCK_INSPECTOR = 's_yelu.utils.block_inspector.inspect_status_code'
