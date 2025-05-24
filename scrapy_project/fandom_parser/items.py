#items.py
import scrapy

class CelestePageItem(scrapy.Item):
    doc_id        = scrapy.Field()
    title         = scrapy.Field()
    url           = scrapy.Field()
    categories    = scrapy.Field()
    last_modified = scrapy.Field()
    section       = scrapy.Field()
    full_text     = scrapy.Field()
    image_urls    = scrapy.Field()
    image_captions = scrapy.Field()
    cv_analysis   = scrapy.Field()
    chunks        = scrapy.Field()