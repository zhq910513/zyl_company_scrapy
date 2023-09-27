import logging

from scrapy.crawler import Crawler
from scrapy.http import Request
from scrapy.http import Response
from scrapy.spiders import Spider
from twisted.internet.defer import inlineCallbacks
from txmongo.connection import ConnectionPool

from news_spider.settings import *
from news_spider.settings.pipelines import MONGODB_COLLECTION

logger = logging.getLogger(__name__)


class UrlsMarkDownloaderMiddleware(object):
    def __init__(self, crawler: Crawler, *args, **kwargs):
        self.crawler = crawler
        # self.uri = MONGODB_URI.format(host=MONGODB_HOST, db=MONGODB_DATABASE)
        self.uri = MONGODB_URI.format(usr=MONGODB_USERNAME, pwd=MONGODB_PASSWORD, host=MONGODB_HOST, db=MONGODB_DATABASE)
        self.db_name = MONGODB_DATABASE
        self.field_name = 'status'
        self.cnx = ConnectionPool(self.uri)
        self.db = getattr(self.cnx, self.db_name)

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args, **kwargs):
        o = cls(crawler=crawler, *args, **kwargs)
        return o

    @inlineCallbacks
    def process_request(self, request: Request, spider: Spider):
        yield request

    def process_response(self, request: Request, response: Response, spider: Spider):
        coll_name = MONGODB_COLLECTION
        coll = getattr(self.db, coll_name)
        if response.status == 200:
            print(request.meta["info"])

        coll.update_one(
            {'hash_key': request.meta['info']['hash_key']},
            {'$set': {
                self.field_name: response.status
            }}
        )
        return response
