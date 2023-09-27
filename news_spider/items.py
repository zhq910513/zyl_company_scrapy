from scrapy.item import Field
from scrapy.item import Item

# 链接表
class URLItem(Item):
    _id = Field()
    hash_key = Field()  # 链接关联字段
    company_name = Field()  # 公司名
    page_url = Field()  # 链接
    page_source_url = Field()  # 页面来源链接
    source_keywords = Field()  # 页面来源关键词


# 页面信息表
class PAGEItem(Item):
    _id = Field()
    hash_key = Field()  # 章节唯一标识
    company_name = Field()  # 公司名
    page_url = Field()  # 当前页面链接
    page_title = Field()  # 页面标题
    page_description = Field()  # 页面描述
    page_keywords = Field()  # 页面关键词
    page_text = Field()  # 页面文本
    page_source_url = Field()  # 页面来源链接
    source_keywords = Field()  # 页面来源关键词
    all_domain = Field()  # 页面所有域名


# 网页源码表
class SOURCEEItem(Item):
    _id = Field()
    hash_key = Field()  # 唯一标识
    page_source_code = Field()  # 源码




