from . import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update({
    'news_spider.downloadermiddlewares.bind_ip_cookies.CookiesMiddleware': 780
})

COOKIES_ENABLED = True
