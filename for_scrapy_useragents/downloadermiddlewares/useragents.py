"""Set User-Agent header per spider or use a default value from settings"""

import logging
from collections import Iterable
from itertools import chain
from itertools import cycle

import json
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import load_object

logger = logging.getLogger(__name__)


class UserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Scrapy'):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENT'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)


class UserAgentsMiddleware(object):
    """
    params:
    USER_AGENTS_ENABLE: bool, control middleware status, open or close
    USER_AGENT: str, compatible with raw middleware
    USER_AGENTS: list,
    USER_AGENTS_STORAGE: str, storage user_agents object, get_user_agents method
    USER_AGENTS_TYPE: str, choice agent type: chrome or firefox ...
    USER_AGENTS_DEVICE: str, choice agent device: mobile or web
    USER_AGENTS_BIND_PROXY: bool, control whether to bind proxy
    """

    def __init__(self, settings, user_agent='Scrapy'):
        self.settings = settings
        self.user_agent = user_agent
        self.user_agents = None
        self.bind_proxy_user_agents = {}
        self.bind_proxy = False
        self.bind_proxy_path = None

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('USER_AGENTS_ENABLE'):
            raise NotConfigured
        o = cls(crawler.settings, crawler.settings['USER_AGENT'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)
        user_agents = self.settings.get('USER_AGENTS')
        object_storage = self.settings.get('USER_AGENTS_STORAGE')
        if not isinstance(user_agents, Iterable) and user_agents is not None:
            raise TypeError('USER_AGENTS should be a iterable or '
                            'None, which get {}'.format(type(user_agents)))
        elif not user_agents:
            user_agents = []

        if user_agents or object_storage:
            self.user_agent = None

        if object_storage:
            user_agents = chain(self.get_storage(object_storage), user_agents)
        if user_agents:
            user_agents = self.user_agents_filter(user_agents)
            self.user_agents = cycle(user_agents)
            next(self.user_agents)
        bind_proxy = self.settings.get('USER_AGENTS_BIND_PROXY')
        if bind_proxy:
            self.bind_proxy_path = self.settings.get(
                'USER_AGENTS_BIND_PATH', 'bind_proxy_user_agents.json')
            self.bind_proxy = True
            try:
                with open(self.bind_proxy_path, 'r') as f:
                    self.bind_proxy_user_agents = json.loads(f.read())
            except Exception as exc:
                logger.error(exc)

    def user_agents_filter(self, user_agents):
        filter_type = self.settings.get('USER_AGENTS_TYPE')
        filter_device = self.settings.get('USER_AGENTS_DEVICE')
        if filter_type:
            user_agents = filter(
                lambda x: x['type'] == filter_type, user_agents)
        if filter_device:
            user_agents = filter(
                lambda x: x['device'] == filter_device, user_agents)
        return map(lambda x: x['user_agent'].strip(), user_agents)

    def get_storage(self, object_storage: str):
        o_storage = load_object(object_storage)
        if isinstance(o_storage, type):
            instance_storage = o_storage(self.settings)
            return instance_storage.get_user_agents()
        elif hasattr(o_storage, '__call__'):
            return o_storage(self.settings)
        else:
            raise TypeError('USER_AGENTS_STORAGE should be a callable or '
                            'class that include get_user_agents method, '
                            'which get {}'.format(o_storage))

    def spider_closed(self):
        if self.bind_proxy_user_agents:
            try:
                with open(self.bind_proxy_path, 'w') as f:
                    f.write(json.dumps(self.bind_proxy_user_agents))
            except Exception as exc:
                logger.error(exc)

    def default_process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)
        if self.user_agents:
            request.headers.setdefault(b'User-Agent', next(self.user_agents))

    def process_bind_proxy(self, request, spider):
        proxy_byte = request.meta.get('proxy')

        if proxy_byte:
            proxy = proxy_byte.decode() if isinstance(proxy_byte, bytes) \
                else proxy_byte
            user_agent = self.bind_proxy_user_agents.get(proxy) or \
                next(self.user_agents)
            self.bind_proxy_user_agents.setdefault(proxy, user_agent)
            request.headers.setdefault(b'User-Agent', user_agent)
        else:
            logger.warning(
                'Proxy not found, please inspect middleware priority, '
                'user-agent will do not bind proxy')
            self.bind_proxy = False
            self.default_process_request(request, spider)

    def process_request(self, request, spider):
        if self.bind_proxy:
            self.process_bind_proxy(request, spider)
        else:
            self.default_process_request(request, spider)

