#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: the king
@project: zyl_company_scrapy
@file: web_chrome.py
@time: 2023/7/4 18:56
"""
import requests
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from news_spider.settings.pipelines import CHROME_DRIVER_PATH
requests.packages.urllib3.disable_warnings()

class SeleniumMiddleware(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument('--headless')  # 可选，如果希望无界面运行
        self.driver = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER_PATH)
        self.driver.set_page_load_timeout(10)
        self.req_session = requests.session()

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            body = str.encode(self.driver.page_source)
            return HtmlResponse(
                url=self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request,
                status=self.req_status(request.url)
            )
        except:
            return HtmlResponse(
                url=request.url,
                body=None,
                encoding='utf-8',
                request=request,
                status=self.req_status(request.url)
            )

    def req_status(self, url):
        try:
            domain_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Sec-Ch-Ua-Platform": '"Windows"',
            }
            resp = self.req_session.get(url=url, headers=domain_headers, verify=False)
            return resp.status_code
        except:
            return 600
