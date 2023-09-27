import hashlib
import sys
from os.path import abspath
from os.path import dirname

from pymongo import MongoClient
from pymongo.errors import CursorNotFound
from scrapy.crawler import CrawlerProcess
from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings

root_path = dirname(dirname(abspath(__file__)))
sys.path.append(root_path)

client = MongoClient('mongodb://readWrite:readWrite123456@127.0.0.1:27017/zyl_company_scrapy')
# client = MongoClient('mongodb://readWrite:readWrite123456@27.150.182.135:27017/zyl_company_scrapy')
website_coll = client['zyl_company_scrapy']['website']
urls_coll = client['zyl_company_scrapy']['urls']


def start_urls():
    status = True
    while status:
        try:
            # 检测每次新增的网站
            for url in website_coll.find({}):
                page_url = url["link"]
                website_coll.update_one({"link": page_url}, {"$set": {"status": 1}}, upsert=True)

                if not str(page_url).startswith("https://") and not str(page_url).startswith(f"http://"):
                    for scheme in [
                        "http://",
                        "https://"
                    ]:
                        new_link = scheme + page_url
                        hash_key = hashlib.md5(str(new_link).encode("utf8")).hexdigest()
                        urls_coll.update_one({"hash_key": hash_key}, {"$set": {
                            "company_name": url["company_name"],
                            "page_url": new_link,
                            "page_source_url": None,
                            "source_keywords": None
                        }}, upsert=True)
                else:
                    hash_key = hashlib.md5(str(page_url).encode("utf8")).hexdigest()
                    urls_coll.update_one({"hash_key": hash_key}, {"$set": {
                        "company_name": url["company_name"],
                        "page_url": page_url,
                        "page_source_url": None,
                        "source_keywords": None
                    }}, upsert=True)

            # 消耗链接池
            if not urls_coll.find_one({"status": None}):
                status = False
                break
            else:
                for url in urls_coll.find({"status": None}):
                    yield url
        except CursorNotFound:
            yield from start_urls()


modules = (
    'concurrent',
    'log',
    # 'job',
    # 'logstats',
    'pipelines',
    # 'proxy_management',
    # 'useragents',
    # 'cookies',
)

if __name__ == '__main__':
    info_list = urls_coll.find({"status": None})
    _settings = get_project_settings()
    for module in modules:
        _settings.setmodule(
            module='news_spider.settings.{}'.format(module)
        )
    # _settings.update({
    #     'HTTPPROXY_MONGODB_COLLECTION': 'proxy_1'
    # })

    spider = load_object(
        'news_spider.spiders.get_urls.UrlSpider'
    )
    process = CrawlerProcess(settings=_settings)
    process.crawl(spider, start_urls=start_urls())
    process.start()
