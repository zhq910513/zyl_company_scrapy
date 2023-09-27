import copy
import hashlib
import logging
import pprint
import re
from typing import Generator
from urllib.parse import urlparse
import scrapy
from bs4 import BeautifulSoup
from pymongo import MongoClient
from scrapy.http import Request
from scrapy.http import Response
from scrapy.item import Item
from scrapy.spiders import Spider

from news_spider.items import URLItem, PAGEItem, SOURCEEItem

pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)

domain_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Authority": "metruyencv.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Sec-Ch-Ua-Platform": '"Windows"',
    }


class UrlSpider(Spider):
    name = 'search_urls'

    def __init__(self, name=None, **kwargs):
        super(UrlSpider, self).__init__(name, **kwargs)
        self.start_urls = kwargs.get('start_urls')

    def start_requests(self):
        for info in self.start_urls:
            if str(info["page_url"]).startswith("http"):
                yield Request(url=info["page_url"], headers=domain_headers, callback=self.parse, meta={'info': info})

    def parse(self, response: Response, **kwargs) -> Generator[Item, None, None]:
        info = response.meta.get('info')
        format_page_info, format_source_info, url_list = self.parse_page_info(info, response)
        # self.parse_page_info(info, response)

        yield PAGEItem({
            "hash_key": format_page_info["hash_key"],
            "company_name": format_page_info["company_name"],
            "page_url": format_page_info["page_url"],
            "page_title": format_page_info["page_title"],
            "page_description": format_page_info["page_description"],
            "page_keywords": format_page_info["page_keywords"],
            "page_text": format_page_info["page_text"],
            "page_source_url": format_page_info["page_source_url"],
            "source_keywords": format_page_info["source_keywords"],
            "all_domain": format_page_info["all_domain"]
        })

        yield SOURCEEItem({
            "hash_key": format_source_info["hash_key"],
            "page_source_code": format_source_info["page_source_code"]
        })

        if url_list:
            for url_info in url_list:
                yield URLItem({
                "hash_key": url_info["hash_key"],
                "company_name": url_info["company_name"],
                "page_url": url_info["page_url"],
                "page_source_url": url_info["page_source_url"],
                "source_keywords": url_info["source_keywords"],
                })

    def parse_page_info(self, info, response):
        try:
            _list, hash_list = [], []
            format_page_info = {
                "hash_key": info["hash_key"],
                "company_name": info["company_name"],
                "page_url": info["page_url"],
                "page_title": "",
                "page_description": "",
                "page_keywords": "",
                "page_text": "",
                "page_source_url": info.get("page_source_url"),
                "source_keywords": info.get("source_keywords"),
                "all_domain": []
            }
            format_url_info = {
                "hash_key": "",
                "company_name": info["company_name"],
                "page_url": "",
                "page_source_url": "",
                "source_keywords": "",
            }
            scheme = urlparse(info["page_url"]).scheme
            domain = urlparse(info["page_url"]).netloc
            all_domain = []
            soup = BeautifulSoup(scrapy.Selector(response).extract(), "lxml")
            try:
                all_domain = list(set(re.findall(r'http[^\/]{1,2}//([^(\/| |")]+)', str(soup))))
            except:
                pass
            # page_title
            page_title = None
            try:
                page_title = soup.find("meta", {"name": "Titles"})
                if page_title:
                    page_title = page_title.get("content")
                if not page_title:
                    page_title = soup.find("meta", {"name": "title"})
                    if page_title:
                        page_title = page_title.get("content")
                if not page_title:
                    page_title = soup.find("title")
                    if page_title:
                        page_title = page_title.get_text()
            except:
                pass

            # page_description
            page_description = None
            try:
                page_description = soup.find("meta", {"name": "description"})
                if page_description:
                    page_description = page_description.get("content")
            except:
                pass

            # page_keywords
            page_keywords = None
            try:
                keywords = soup.find("meta", {"name": "Keywords"})
                if keywords:
                    page_keywords = keywords.get("content")
                else:
                    keywords = soup.find("meta", {"name": "keywords"})
                    if keywords:
                        page_keywords = keywords.get("content")
            except:
                pass

            # page_text
            page_text = None
            try:
                page_text = self.deal_text(soup)
            except:
                pass

            format_page_info.update({
                "page_title": page_title,
                "page_description": page_description,
                "page_keywords": page_keywords,
                "page_text":page_text,
                "all_domain": all_domain
            })

            # 子链接
            try:
                for a in soup.find_all("a"):
                    url_data = copy.deepcopy(format_url_info)
                    href = a.get("href")
                    if str(href).endswith(".html"):
                        page_url = self.format_img_url(scheme, domain, href)
                        if page_url and str(page_url).startswith("http"):
                            url_data["page_url"] = page_url
                            url_data["hash_key"] = hashlib.md5(str(page_url).encode("utf8")).hexdigest()
                            url_data["page_source_url"] = format_page_info.get("page_url")
                            url_data["source_keywords"] = page_keywords

                            if url_data["hash_key"] not in hash_list:
                                hash_list.append(url_data["hash_key"])
                                _list.append(url_data)
            except:
                pass

            format_source_info = {
                "hash_key": info["hash_key"],
                "page_source_code": str(soup)
            }

            return format_page_info, format_source_info, _list
        except Exception as error:
            logger.error(error)

    @staticmethod
    def deal_text(soup):
        # rough clean
        while soup.link:
            soup.link.extract()
        while soup.script:
            soup.script.extract()
        while soup.style:
            soup.style.extract()
        raw_content = list(soup.stripped_strings)
        return raw_content

    def format_img_url(self, scheme, domain, href):
        # http://www.abc.com   https://www.abc.com
        link_header = f"{scheme}://{domain}"
        try:
            if 'http' not in href and 'https' not in href:
                # ://www.abc.com
                if str(href).startswith(':'):
                    href = scheme + href
                # //www.abc.com
                elif str(href).startswith('//'):
                    href = scheme + ":" + href
                # /www.abc.com     /defg.hijk.html
                elif str(href).startswith('/'):
                    # /defg.hijk.html
                    if domain not in href:
                        href = link_header + href
                    # /www.abc.com
                    else:
                        href = f"{scheme}:/" + href
                # ..://www.abc.com    ..//www.abc.com    ../www.abc.com    ../defg.hijk.html
                elif str(href).startswith('..'):
                    return self.format_img_url(scheme, domain, href.replace('../', ''))
                else:
                    href = None
            else:
                if domain not in href:
                    href = None
        except:
            href = None
        if href:
            if not str(href).startswith("http"):
                href = None
            else:
                href_scheme = urlparse(href).scheme
                href_domain = urlparse(href).netloc
                href_link_header = f"{href_scheme}://{href_domain}"
                if link_header != href_link_header:
                    href = href.replace(href_link_header, link_header)
        return href