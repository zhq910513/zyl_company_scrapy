from pymongo import MongoClient
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy_pipeline_mongodb.pipelines.mongodb_async import PipelineMongoDBAsync
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def process_item(pipeline: PipelineMongoDBAsync, item: Item, spider: Spider) -> Item:
    client = MongoClient('mongodb://sbdrg:Aa123654@10.0.0.4:27017/search-engine')
    coll = client['search-engine']['facebook_company_urls']
    print(item)
    yield pipeline.coll.update_one(
        {'homepage_link': item['homepage_link']},
        {'$set': dict(item)},
        upsert=True
    )
    try:
        coll.update_one({'facebook_url': item['homepage_link']}, {'$set': {'check_status': 'used'}}, upsert=True)
    except:
        pass
