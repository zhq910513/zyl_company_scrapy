from . import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'for_scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 800
})

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENTS_ENABLE = True
# USER_AGENT = None
# USER_AGENTS = None
USER_AGENTS_STORAGE = 'for_scrapy_useragents.utils.storage.FileStorage'
USER_AGENTS_FILE_PATH = '../for_scrapy_useragents/utils/user_agents.json'
USER_AGENTS_TYPE = 'Chrome'
USER_AGENTS_DEVICE = 'web'
USER_AGENTS_BIND_PROXY = True
