from ..settings import *

# -----------------------------------------------------------------------------
# HTTPCACHE
# -----------------------------------------------------------------------------

DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
    'scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware': 900,
})

HTTPCACHE_ENABLED = True

HTTPCACHE_STORAGE = 'scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage'

HTTPCACHE_MONGODB_HOST = MONGODB_HOST
HTTPCACHE_MONGODB_PORT = 27017

HTTPCACHE_MONGODB_USERNAME = HTTPCACHE_MONGODB_USERNAME
HTTPCACHE_MONGODB_PASSWORD = HTTPCACHE_MONGODB_PASSWORD

HTTPCACHE_MONGODB_DB = HTTPCACHE_MONGODB_DB
HTTPCACHE_MONGODB_AUTH_DB = HTTPCACHE_MONGODB_AUTH_DB

HTTPCACHE_MONGODB_COLL = HTTPCACHE_MONGODB_COLL

HTTPCACHE_IGNORE_HTTP_CODES = [301, 302, 404, 407, 500, 502, 503]
