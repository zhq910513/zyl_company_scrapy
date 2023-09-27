from pymongo import MongoClient
from twisted.internet.defer import inlineCallbacks

from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy_pipeline_mongodb.pipelines.mongodb_async import PipelineMongoDBAsync

from pymongo.errors import DuplicateKeyError


@inlineCallbacks
def process_item(
        pipeline: PipelineMongoDBAsync,
        item: Item,
        spider: Spider
) -> Item:
    client = MongoClient('mongodb://readWrite:readWrite123456@127.0.0.1:27017/zyl_company_scrapy')
    # client = MongoClient('mongodb://readWrite:readWrite123456@27.150.182.135:27017/zyl_company_scrapy')

    page_coll = client['zyl_company_scrapy']['page_info']
    source_coll = client['zyl_company_scrapy']['page_source']
    urls_coll = client['zyl_company_scrapy']['urls']


    # 文章内容  后改S3
    if not item.get("company_name"):
        try:
            yield source_coll.insert_one(
                item
            )
        except DuplicateKeyError:
            pass
    else:
        if item.get("page_text"):
            try:
                yield page_coll.insert_one(
                    item
                )
            except DuplicateKeyError:
                pass
        else:
            try:
                yield urls_coll.insert_one(
                    item
                )
            except DuplicateKeyError:
                pass